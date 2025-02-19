# Botify

Botify is a document processing and retrieval system that leverages the power of LangChain and OpenAI technologies. It provides various utilities for processing different types of documents and retrieving information efficiently.

## Project Structure

- `common/preprocessing/preprocessor.py`: Contains classes and methods for document processing and splitting.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### DocumentProcessorFactory

The `DocumentProcessorFactory` class provides methods to build processors for different types of documents.

```python
from common.preprocessing.preprocessor import DocumentProcessorFactory

factory = DocumentProcessorFactory()
factory.build_audio_processor()  # Not implemented yet
factory.build_image_processor()  # Not implemented yet
factory.build_doc_processor()    # Not implemented yet
```

### Splitter

The `Splitter` class is used to split documents into smaller chunks.

```python
from common.preprocessing.preprocessor import Splitter

splitter = Splitter(chunk_size=500, chunk_overlap=0)
chunks = splitter.split_docs(langchain_text)
```

## Dependencies

- `langchain`
- `langchain_community`
- `langchain_openai`

## License

This project is licensed under the MIT License.