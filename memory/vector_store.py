import os
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class VectorStore:
    def __init__(self, persist_dir: str) -> None:
        os.makedirs(persist_dir, exist_ok=True)
        self.persist_dir = persist_dir
        self._emb = OpenAIEmbeddings()
        self._store = None

    def _get_store(self):
        if self._store is None:
            self._store = Chroma(
                collection_name="study_buddy",
                embedding_function=self._emb,
                persist_directory=self.persist_dir,
            )
        return self._store

    def ingest_folder(self, folder: str, chunk_size: int = 800, chunk_overlap: int = 120) -> int:
        texts = []
        metadatas = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for root, _, files in os.walk(folder):
            for f in files:
                path = os.path.join(root, f)
                if not os.path.isfile(path):
                    continue
                with open(path, "r", encoding="utf-8") as fh:
                    content = fh.read()
                for chunk in splitter.split_text(content):
                    texts.append(chunk)
                    metadatas.append({"source": path})
        if not texts:
            return 0
        store = self._get_store()
        store.add_texts(texts=texts, metadatas=metadatas)
        store.persist()
        return len(texts)

    def search(self, query: str, k: int = 4) -> List[str]:
        store = self._get_store()
        docs = store.similarity_search(query, k=k)
        return [d.page_content for d in docs]
