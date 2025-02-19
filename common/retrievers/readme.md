# Botify Retrievers

This module provides various retrievers for document search and retrieval. The retrievers included are:

- `BaseVectorStoreRetriever`
- `BM25LexicalRetriever`
- `HybridRetriever`

## Retrievers

### BaseVectorStoreRetriever

A retriever that uses a vector store for document retrieval.

#### Initialization

```python
BaseVectorStoreRetriever(vector_store, top_k=80, threshold=None, search_type='mmr')
```

- `vector_store`: The vector store to use for retrieval.
- `top_k`: The number of top documents to retrieve.
- `threshold`: The score threshold for retrieval.
- `search_type`: The type of search to perform.

#### Methods

- `invoke(query, config=None)`: Invokes the retriever with the given query and configuration.

### BM25LexicalRetriever

A retriever that uses BM25 for lexical document retrieval.

#### Initialization

```python
BM25LexicalRetriever(docs, top_k=80, vectorizer=None, preprocess_func=default_preprocessing_func)
```

- `docs`: The documents to use for retrieval.
- `top_k`: The number of top documents to retrieve.
- `vectorizer`: The vectorizer to use for BM25.
- `preprocess_func`: The preprocessing function to use.

#### Methods

- `invoke(query, config=None)`: Invokes the retriever with the given query and configuration.

### HybridRetriever

A hybrid retriever that combines vector store and BM25 lexical retrieval.

#### Initialization

```python
HybridRetriever(vector_store, documents, alpha=0.6, top_k=80, search_type='mmr', threshold=None)
```

- `vector_store`: The vector store to use for retrieval.
- `documents`: The documents to use for BM25 retrieval.
- `alpha`: The weight for the vector store retriever.
- `top_k`: The number of top documents to retrieve.
- `search_type`: The type of search to perform.
- `threshold`: The score threshold for retrieval.

#### Methods

- `invoke(query, config=None)`: Invokes the retriever with the given query and configuration.

## Example Usage

```python
from botify.common.retrievers.retriever import BaseVectorStoreRetriever, BM25LexicalRetriever, HybridRetriever

# Example initialization and usage
vector_store = ...  # Initialize your vector store
documents = [...]  # List of documents

# BaseVectorStoreRetriever
base_retriever = BaseVectorStoreRetriever(vector_store)
results = base_retriever.invoke("example query")

# BM25LexicalRetriever
bm25_retriever = BM25LexicalRetriever(documents)
results = bm25_retriever.invoke("example query")

# HybridRetriever
hybrid_retriever = HybridRetriever(vector_store, documents)
results = hybrid_retriever.invoke("example query")
```