from uuid import uuid4
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import faiss


class VectorStore:

    def __init__(self, embeddings_provider, store_name="FAISS", index=None):
        self._embeddings_provider = embeddings_provider
        self._index = index
        match store_name:
            case "FAISS":
                doc_store = InMemoryDocstore()
                self._index = faiss.IndexFlatL2(
                    len(self._embeddings_provider.embeddings.embed_query("hello world"))
                )
                self._store = FAISS_VECTOR_STORE(
                    doc_store=doc_store,
                    embedding_function=self._embeddings_provider,
                    index=self._index,
                    index_to_docstore_id={},
                )

    @property
    def store(self):
        return self._store


class FAISS_VECTOR_STORE(FAISS):

    class Config:
        arbitrary_types_allowed = True

    _embeddings_function = None

    def __init__(self, **kwargs):
        if "doc_store" in kwargs:
            self._doc_store = kwargs["doc_store"]
        if "index" in kwargs:
            self._index = kwargs["index"]
            del kwargs["index"]
        if "index_to_docstore_id" in kwargs:
            self._index_to_docstore_id = kwargs["index_to_docstore_id"]
            del kwargs["index_to_docstore_id"]
        if "embedding_function" in kwargs:
            self._embedding_function = kwargs["embedding_function"]
            del kwargs["embedding_function"]

        super().__init__(
            docstore=self._doc_store,
            embedding_function=self._embedding_function.embeddings,
            index=self._index,
            index_to_docstore_id=self._index_to_docstore_id,
        )

    def add_documents(self, documents, uuids=None):
        uuids = uuids or [str(uuid4()) for _ in range(len(documents))]
        super().add_documents(documents=documents, ids=uuids)
