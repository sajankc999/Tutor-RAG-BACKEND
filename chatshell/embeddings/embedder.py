from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from django.conf import settings
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001"
# )

vector_store = Chroma(
    collection_name="uploaded-file",
    embedding_function=embeddings,
    persist_directory="chroma"
)


# vector_store = InMemoryVectorStore(embedding=embeddings)
# vector_store = InMemoryVectorStore(OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY))
