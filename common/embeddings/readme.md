# EmbeddingProvider

The `EmbeddingProvider` class is a utility for managing different types of embeddings from various providers. It supports embeddings from Sentence Transformer, OpenAI, and NVIDIA.

## Initialization

To initialize the `EmbeddingProvider`, you need to specify the embedding provider and optionally the model name.

```python
from common.embeddings.embeddings import EmbeddingProvider

# Initialize with Sentence Transformer
provider = EmbeddingProvider(embedding_provider="sentence-transformer", model_name="BAAI/bge-multilingual-gemma2")

# Initialize with OpenAI
provider = EmbeddingProvider(embedding_provider="open-ai", model_name="text-embedding-3-large")

# Initialize with NVIDIA
provider = EmbeddingProvider(embedding_provider="NVIDIA", model_name="NV-Embed-v2")
```

If the model name is not provided, default models will be used:
- Sentence Transformer: `BAAI/bge-multilingual-gemma2`
- OpenAI: `text-embedding-3-large`
- NVIDIA: `NV-Embed-v2`

## Accessing Embeddings

You can access the embeddings through the `embeddings` property.

```python
embeddings = provider.embeddings
```

This will return the embeddings object from the specified provider.