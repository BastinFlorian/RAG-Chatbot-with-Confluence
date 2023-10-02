import sys
import logging
import shutil

sys.path.append('../')
from config import (CONFLUENCE_SPACE_NAME, CONFLUENCE_SPACE_KEY,
                    CONFLUENCE_USERNAME, CONFLUENCE_API_KEY, PERSIST_DIRECTORY)

from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter

class DataLoader():
    """Create, load, save the DB using the confluence Loader"""
    def __init__(
        self,
        confluence_url=CONFLUENCE_SPACE_NAME,
        username=CONFLUENCE_USERNAME,
        api_key=CONFLUENCE_API_KEY,
        space_key=CONFLUENCE_SPACE_KEY,
        persist_directory=PERSIST_DIRECTORY
    ):

        self.confluence_url = confluence_url
        self.username = username
        self.api_key = api_key
        self.space_key = space_key
        self.persist_directory = persist_directory

    def load_from_confluence_loader(self):
        """Load HTML files from Confluence"""
        loader = ConfluenceLoader(
            url=self.confluence_url,
            username=self.username,
            api_key=self.api_key
        )

        docs = loader.load(
            space_key=self.space_key,
            # include_attachments=True,
            )
        return docs

    def split_docs(self, docs):
        # Markdown
        headers_to_split_on = [
            ("#", "Titre 1"),
            ("##", "Sous-titre 1"),
            ("###", "Sous-titre 2"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        # Split based on markdown and add original metadata
        md_docs = []
        for doc in docs:
            md_doc = markdown_splitter.split_text(doc.page_content)
            for i in range(len(md_doc)):
                md_doc[i].metadata = md_doc[i].metadata | doc.metadata
            md_docs.extend(md_doc)

        # RecursiveTextSplitter
        # Chunk size big enough
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=20,
            separators=["\n\n", "\n", "(?<=\. )", " ", ""]
        )

        splitted_docs = splitter.split_documents(md_docs)
        return splitted_docs

    def save_to_db(self, splitted_docs, embeddings):
        """Save chunks to Chroma DB"""
        from langchain.vectorstores import Chroma
        db = Chroma.from_documents(splitted_docs, embeddings, persist_directory=self.persist_directory)
        db.persist()
        return db

    def load_from_db(self, embeddings):
        """Loader chunks to Chroma DB"""
        from langchain.vectorstores import Chroma
        db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings
        )
        return db

    def set_db(self, embeddings):
        """Create, save, and load db"""
        try:
            shutil.rmtree(self.persist_directory)
        except Exception as e:
            logging.warning("%s", e)

        # Load docs
        docs = self.load_from_confluence_loader()

        # Split Docs
        splitted_docs = self.split_docs(docs)

        # Save to DB
        db = self.save_to_db(splitted_docs, embeddings)

        return db

    def get_db(self, embeddings):
        """Create, save, and load db"""
        db = self.load_from_db(embeddings)
        return db


if __name__ == "__main__":
    pass
