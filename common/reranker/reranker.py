from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors.rankllm_rerank import RankLLMRerank


class CrossEncoder(ContextualCompressionRetriever):

    class Config:
        arbitrary_types_allowed = True


    def __init__(self, base_retriever, model_name = None, top_n = 5):
        model_name = model_name
        if not model_name:
            model_name = "BAAI/bge-reranker-base"
        model = HuggingFaceCrossEncoder(model_name=model_name)
        ranker = CrossEncoderReranker(model=model, top_n=top_n)
        super().__init__(base_compressor = ranker, base_retriever = base_retriever)

    def invoke(self,query):
        return super().invoke(query)



class LLMReranker(ContextualCompressionRetriever):

    class Config:
        arbitrary_types_allowed = True


    def __init__(self, base_retriever, model_name = None, top_n = 5):
        model_name = model_name
        if not self._model_name:
            model_name = "zephyr"
        ranker = RankLLMRerank(model=model_name, top_n=top_n)
        super().__init__(base_compressor = ranker, base_retriever = base_retriever)


    def invoke(self,query):
        return super().invoke(query)

