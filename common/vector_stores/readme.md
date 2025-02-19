# VectorStore

The `VectorStore` class is a wrapper around different vector store implementations, such as FAISS, to provide a unified interface for storing and retrieving vector embeddings.

## Installation

Ensure you have the required dependencies installed:

```bash
pip install langchain langchain_community langchain_openai faiss-cpu
```

## Usage

### Initialization

To initialize a `VectorStore` instance, you need to provide an embeddings provider and optionally specify the store name (default is "FAISS").

```python
from your_embeddings_provider import YourEmbeddingsProvider
from vector_store import VectorStore

embeddings_provider = YourEmbeddingsProvider()
vector_store = VectorStore(embeddings_provider)
```

### Adding Documents

To add documents to the vector store, use the `add_documents` method of the `FAISS_VECTOR_STORE` class.

```python
documents = ["Document 1 text", "Document 2 text"]
vector_store.store.add_documents(documents)
```

## Classes

### VectorStore

The `VectorStore` class initializes the vector store based on the specified store name.

#### Parameters

- `embeddings_provider`: The provider for generating embeddings.
- `store_name`: The name of the vector store to use (default is "FAISS").
- `index`: Optional index to use for the vector store.

### FAISS_VECTOR_STORE

A subclass of `FAISS` that provides additional configuration and methods for managing the FAISS vector store.

#### Methods

- `add_documents(documents)`: Adds a list of documents to the vector store.

## Example

Here is a complete example of how to use the `VectorStore` class:

```python
from your_embeddings_provider import YourEmbeddingsProvider
from vector_store import VectorStore

# Initialize embeddings provider
embeddings_provider = YourEmbeddingsProvider()

# Initialize vector store
vector_store = VectorStore(embeddings_provider)

# Add documents
documents = ["Document 1 text", "Document 2 text"]
vector_store.store.add_documents(documents)
```