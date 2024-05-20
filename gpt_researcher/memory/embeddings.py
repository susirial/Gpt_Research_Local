from langchain_community.vectorstores import FAISS
import os


class Memory:
    def __init__(self, embedding_provider, **kwargs):

        _embeddings = None
        match embedding_provider:
            case "ollama":
                from langchain.embeddings import OllamaEmbeddings
                _embeddings = OllamaEmbeddings(model="llama2")
            case "openai":
                from langchain_openai import OpenAIEmbeddings
                _embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            case "azureopenai":
                from langchain_openai import AzureOpenAIEmbeddings
                _embeddings = AzureOpenAIEmbeddings(deployment=os.environ["AZURE_EMBEDDING_MODEL"], chunk_size=16)
            case "huggingface":
                from langchain.embeddings import HuggingFaceEmbeddings
                _embeddings = HuggingFaceEmbeddings()
            # Add local bce for windows, you can add your embeddings
            case "local_bce":
                from langchain.embeddings import HuggingFaceEmbeddings
                # 用本地模型路径替换
                embedding_model_name = 'D:\LLM\\bce_modesl\\bce-embedding-base_v1'
                # 使用 GPU
                embedding_model_kwargs = {'device': 'cuda:0'}

                # 使用 CPU
                #embedding_model_kwargs = {'device': 'cpu'}

                embedding_encode_kwargs = {'batch_size': 32, 'normalize_embeddings': True, }

                # 初始化
                embed_model = HuggingFaceEmbeddings(
                    model_name=embedding_model_name,
                    model_kwargs=embedding_model_kwargs,
                    encode_kwargs=embedding_encode_kwargs
                )
                _embeddings = embed_model
            case _:
                raise Exception("Embedding provider not found.")

        self._embeddings = _embeddings

    def get_embeddings(self):
        return self._embeddings
