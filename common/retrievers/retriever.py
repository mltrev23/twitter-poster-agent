from typing import List, Optional

from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document


def default_preprocessing_func(text: str) -> List[str]:
    return text.split()


class BaseVectorStoreRetriever(VectorStoreRetriever):

    def __init__(
        self,
        vector_store,
        top_k: int = 80,
        threshold: Optional[float] = None,
        search_type="mmr",
    ):
        if not threshold:
            super().__init__(
                vectorstore=vector_store,
                search_type=search_type,
                search_kwargs={"k": top_k},
            )
        else:
            super().__init__(
                vectorstore=vector_store,
                search_type=search_type,
                search_kwargs={"score_threshold": threshold, "k": top_k},
            )

    def invoke(self, query, config=None):
        return super().invoke(input=query, config=config)


class BM25LexicalRetriever(BM25Retriever):

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        docs,
        top_k=80,
        vectorizer=None,
        preprocess_func=default_preprocessing_func,
    ):
        super().__init__(
            docs=docs, k=top_k, vectorizer=vectorizer, preprocess_func=preprocess_func
        )

    def invoke(self, query, config=None):
        return super().invoke(input=query, config=config)


class HybridRetriever(EnsembleRetriever):

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        vector_store,
        documents,
        alpha=0.6,
        top_k=80,
        search_type="mmr",
        threshold=None,
    ):
        sparse_ratio = 1 - alpha
        dense_ratio = alpha
        weights = [dense_ratio, sparse_ratio]
        dense_retriever = BaseVectorStoreRetriever(
            vector_store, top_k=top_k, threshold=threshold, search_type=search_type
        )
        bm25 = BM25LexicalRetriever(top_k=top_k, docs=documents)
        sparse_retriever = bm25.from_documents(documents)
        retrievers = [dense_retriever, sparse_retriever]
        super().__init__(retrievers=retrievers, weights=weights)

    def invoke(self, query, config=None):
        return super().invoke(input=query, config=config)
