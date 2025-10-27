from django.shortcuts import render
from django.views.generic import CreateView
from content.forms import ContentForm
from django.urls import reverse_lazy
from chatshell.embeddings.vector_store import add_vector
from content.serializers import ContentSerializer
from langchain_core.documents import Document
from chatshell.embeddings.embedder import vector_store
from rest_framework.generics import CreateAPIView
from content.models import Content
from rest_framework.parsers import MultiPartParser, FormParser
from chatshell.embeddings.create_database import save_to_chroma,split_text

class ContentCreateview(CreateView):
    form_class = ContentForm
    success_url=reverse_lazy('content:UploadFile')
    template_name="upload-file.html"
    success_message = "File Uploaded successfully"

    def post(self, request, *args, **kwargs):

        response=super().post(request, *args, **kwargs)

        obj=self.object
        
        
        serialized_data = ContentSerializer(obj).data

        document =[ Document(
                            page_content=serialized_data['page_content'],
                            metadata=serialized_data['metadata']
                            )]
        
        # raise Exception(document.page_content)
        chunks = split_text(document)

        save_to_chroma(chunks)

        # vector_store.add_documents(
        #     documents=[document]
        # )



        # top_n = 10
        # for index, (id, doc) in enumerate(vector_store.store.items()):
        #     if index < top_n:
        #         # docs have keys 'id', 'vector', 'text', 'metadata'
        #         print(f"{id}: {doc['text']}")
        #     else:
        #         break
        return response





class ContentCreateAPIView(CreateAPIView):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):

        response=super().post(request, *args, **kwargs)

        obj=self.object
        
        serialized_data = ContentSerializer(obj).data

        document = Document(id=serialized_data['id'],
                            page_content=serialized_data['page_content'],
                            metadata=serialized_data['metadata'])
        vector_store.add_documents(
            documents=[document]
        )

        return response


