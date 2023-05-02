"""Script to upload books to your vector index by running the ask-my-book package remotely."""

from steamship import Steamship
from steamship.utils.url import Verb

# Step 1: Give your database a name
DB_NAME = "your-db-name"

PACKAGE_HANDLE = "ask-my-book-chat-api"

if __name__ == "__main__":
    client = Steamship(workspace=DB_NAME)

    package_instance = client.use(
        PACKAGE_HANDLE,
        fetch_if_exists=True
    )
    print("BASE_URL:", package_instance.invocation_url)
    print(package_instance.package_version_handle)

    docs = package_instance.invoke("documents", verb=Verb.GET)
    print(docs)
    package_instance.invoke("reset", verb=Verb.POST)
    docs = package_instance.invoke("documents", verb=Verb.GET)
    print(docs)
    package_instance.invoke("add_document", **{
        "url": "https://www.pdfdrive.com/download.pdf?id=158699038&h=27b488a11dd3efed1217baf65bf0e102&u=cache&ext=pdf",
        "name": "tester.pdf",
        "mime_type": "application/pdf"
    })
    docs = package_instance.invoke("documents", verb=Verb.GET)
    print(docs)
    response = package_instance.invoke("answer", question="What is specific knowledge?")
    print(response)
