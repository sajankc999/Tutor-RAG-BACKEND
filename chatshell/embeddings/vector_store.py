from langchain_core.documents import Document
from chatshell.embeddings.embedder import vector_store
from celery import shared_task


@shared_task
def add_vector(document_data):
    # raise Exception(document_data)
    document = Document(
        id=document_data['id'],
        page_content=f"""
            content: {document_data['page_content']},
            metadata:(
                {document_data['metadata']}
            )

        """,
        metadata=document_data['metadata'])
    vector_store.add_documents(
        documents=[document]
    )


# def _filter_function(doc: Document,keyword,value) -> bool:
#     return doc.metadata.get(keyword) == value

@shared_task
def vector_similarity_search(query,no_of_documents=1):
    results = vector_store.similarity_search(query=query, k=no_of_documents)
    return results




