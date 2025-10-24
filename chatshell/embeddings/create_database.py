from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
import os
import shutil
from langchain_text_splitters.character import RecursiveCharacterTextSplitter


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


DATA_PATH = 'media/contents'
CHROMA_PATH = 'chroma'


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def save_to_chroma(chunks:list[Document]):

    if not os.path.exists(CHROMA_PATH):
        os.mkdir(CHROMA_PATH)
    db = Chroma(
        collection_name='uploaded-file',
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH

    )
    db.add_documents(chunks)
    # db.persist()

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob=["*.md",'*.txt','*.doc'])
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks

