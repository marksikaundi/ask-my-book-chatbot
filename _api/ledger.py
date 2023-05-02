from steamship import File, Steamship, SteamshipError, Tag

TAG_KEY = "book_name"


class Ledger:
    """Class to keep track of the files that were uploaded to the index."""

    def __init__(self, client: Steamship, index_name: str):
        self.client = client
        self._ledger_file = self._get_or_create_ledger_file(index_name)

    def _get_or_create_ledger_file(self, index_name: str) -> File:
        try:
            return File.get(self.client, handle=index_name)
        except SteamshipError:
            return File.create(self.client, handle=index_name, tags=[])

    def add_document(self, name: str):
        Tag.create(
            client=self.client,
            file_id=self._ledger_file.id,
            kind=TAG_KEY,
            name=name,
        )

    def list_documents(self):
        tags = self._ledger_file.refresh().tags
        return [tag.name for tag in tags if tag.kind == TAG_KEY]

    def reset(self):
        for tag in self._ledger_file.refresh().tags:
            tag.client = self.client
            tag.delete()