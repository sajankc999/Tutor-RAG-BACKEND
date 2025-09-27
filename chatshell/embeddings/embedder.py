from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from django.conf import settings
from langchain_community.embeddings import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vector_store = InMemoryVectorStore(embedding=embeddings)
# vector_store = InMemoryVectorStore(OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY))


