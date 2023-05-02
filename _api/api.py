import re
from typing import Type, Optional, Dict, Any, List

import langchain
from langchain.chains import ChatVectorDBChain
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PagedPDFSplitter
from pydantic.networks import HttpUrl
from steamship import MimeTypes, SteamshipError
from steamship import Steamship
from steamship.data.embeddings import EmbeddingIndex
from steamship.invocable import Config
from steamship.invocable import PackageService, post, get
from steamship_langchain.llms.openai import OpenAIChat
from steamship_langchain.vectorstores import SteamshipVectorStore

from chat_history import ChatHistory
from constants import DEBUG
from fact_checker import FactChecker
from ledger import Ledger
from prompts import CONDENSE_QUESTION_PROMPT, ANSWER_QUESTION_PROMPT_SELECTOR

langchain.llm_cache = None
import requests
from pathlib import Path

SUPPORTED_MIME_TYPES = {
    MimeTypes.PDF
}


class AskMyBook(PackageService):
    class AskMyBookConfig(Config):
        model_name: str = "gpt-3.5-turbo"

    config: AskMyBookConfig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_name = self.client.config.workspace_handle + "_index"
        self.qa_chatbot_chain = self._get_qa_chain()
        self.fact_checker = FactChecker(self.client)
        self.ledger = Ledger(self.client, self.index_name)

    @classmethod
    def config_cls(cls) -> Type[Config]:
        return cls.AskMyBookConfig

    @post("/add_document")
    def add_document(self,
                     url: HttpUrl,
                     name: str,
                     mime_type: Optional[MimeTypes] = None) -> bool:
        if mime_type not in SUPPORTED_MIME_TYPES:
            raise SteamshipError("Unsupported mimeType")

        file_path = Path('/tmp/' + name)
        with file_path.open("wb") as f:
            f.write(requests.get(url).content)

        self.add_document_from_path(file_path, name)
        return True

    def add_document_from_path(self, file_path, name) -> None:
        doc_index = self._get_index()
        loader = PagedPDFSplitter(str(file_path.resolve()))
        pages = loader.load_and_split()
        doc_index.add_texts(
            texts=[re.sub("\u0000", "", page.page_content) for page in pages],
            metadatas=[{**page.metadata, "source": name} for page in pages],
        )
        self.ledger.add_document(name)

    @get("/documents", public=True)
    def get_indexed_documents(self) -> List[str]:
        """Fetch all the documents in the index"""
        return self.ledger.list_documents()

    @post("/reset")
    def reset(self) -> bool:
        """Fetch all the documents in the index"""
        doc_index = self._get_index()
        doc_index.index.index.delete()
        doc_index.index.index = EmbeddingIndex.create(
            client=self.client,
            handle=doc_index.index.handle,
            embedder_plugin_instance_handle=doc_index.index.embedder.handle,
            fetch_if_exists=False,
        )
        self.ledger.reset()
        return True

    @post("/answer", public=True)
    def answer(
            self, question: str, chat_session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Answer a given question using a collection of source documents."""
        chat_session_id = chat_session_id or "default"
        chat_history = ChatHistory(self.client, chat_session_id)

        result = self.qa_chatbot_chain(
            {"question": question, "chat_history": chat_history.load()}
        )
        sources = result["source_documents"]
        if len(sources) == 0:
            return {
                "answer": "No sources found to answer your question. Please try another question.",
                "sources": sources,
                "is_plausible": True,
            }

        answer = result["answer"].strip()
        chat_history.append(question, answer)
        is_plausible = self.fact_checker.fact_check(question, answer, sources)

        return {
            "answer": answer,
            "sources": sources,
            "is_plausible": is_plausible,
        }

    def _get_index(self):
        """Get the vector store index."""
        return SteamshipVectorStore(
            client=self.client,
            index_name=self.index_name,
            embedding="text-embedding-ada-002",
        )

    def _get_qa_chain(self):
        """Construct the question answering chain."""
        doc_index = self._get_index()

        llm = OpenAIChat(client=self.client, model_name=self.config.model_name, temperature=0, verbose=DEBUG)
        answer_question_chain = load_qa_chain(
            llm,
            chain_type="stuff",
            prompt=ANSWER_QUESTION_PROMPT_SELECTOR.get_prompt(llm),
            verbose=DEBUG,
        )
        condense_question_chain = LLMChain(
            llm=OpenAIChat(client=self.client, model_name=self.config.model_name, temperature=0, verbose=DEBUG),
            prompt=CONDENSE_QUESTION_PROMPT,
        )
        return ChatVectorDBChain(
            vectorstore=doc_index,
            combine_docs_chain=answer_question_chain,
            question_generator=condense_question_chain,
            return_source_documents=True,
            top_k_docs_for_context=2,
        )


if __name__ == '__main__':
    db_name = "your-db-name"
    client = Steamship(workspace=db_name)
    amb = AskMyBook(client)

    print(amb.get_indexed_documents())
    # response = amb.answer("What is the color of a banana?")
    # print(response)
    #
    # response = amb.answer("Are you a Trump fan?")
    # print(response)
    #
    # response = amb.answer("Are you a trump fan?")
    # print(response)
