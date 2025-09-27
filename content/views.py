from django.shortcuts import render
from django.views.generic import CreateView
from content.forms import ContentForm
from django.urls import reverse_lazy
from chatshell.embeddings.vector_store import add_vector
from content.serializers import ContentSerializer



class ContentCreateview(CreateView):
    form_class = ContentForm
    success_url=reverse_lazy('content:UploadFile')
    template_name="upload-file.html"
    success_message = "File Uploaded successfully"

    def post(self, request, *args, **kwargs):

        response=super().post(request, *args, **kwargs)

        obj=self.object
        
        serialized_data = ContentSerializer(obj).data

        add_vector.delay(
            document_data=serialized_data

        )

        return response





