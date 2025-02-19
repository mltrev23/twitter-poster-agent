# Botify Rerankers

This module contains implementations of rerankers using different models.

## Classes

### CrossEncoder

A reranker that uses a cross-encoder model for ranking documents.

#### Initialization

```python
CrossEncoder(base_retriever, model_name=None, top_n=5)
```

- `base_retriever`: The base retriever to use.
- `model_name`: The name of the cross-encoder model to use. Defaults to `"BAAI/bge-reranker-base"`.
- `top_n`: The number of top documents to return. Defaults to `5`.

#### Methods

- `invoke(query)`: Invokes the reranker with the given query.

### LLMReranker

A reranker that uses a large language model (LLM) for ranking documents.

#### Initialization

```python
LLMReranker(base_retriever, model_name=None, top_n=5)
```

- `base_retriever`: The base retriever to use.
- `model_name`: The name of the LLM model to use. Defaults to `"zephyr"`.
- `top_n`: The number of top documents to return. Defaults to `5`.

#### Methods

- `invoke(query)`: Invokes the reranker with the given query.