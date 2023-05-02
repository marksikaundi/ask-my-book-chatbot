from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains.prompt_selector import (
    ConditionalPromptSelector,
    is_chat_model,
)

CONDENSE_QUESTION_PROMPT_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    CONDENSE_QUESTION_PROMPT_TEMPLATE
)


prompt_template = """Use the following pieces of context to answer the question at the end. If you cannot answer the question with the given CONTEXT, just say that you don't know, don't try to make up an answer.

context: {context}

question: {question}

answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

system_template = """Use the following pieces of context to answer the users question. 
If you cannot answer the question with the given context, just say that you don't know, don't try to make up an answer.
----------------
{context}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)

ANSWER_QUESTION_PROMPT_SELECTOR = ConditionalPromptSelector(
    default_prompt=PROMPT, conditionals=[(is_chat_model, CHAT_PROMPT)]
)
