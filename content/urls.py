from django.urls import path
from content.views import ContentCreateview


app_name="content"

urlpatterns = [
    path(
        "upload-file/",
        ContentCreateview.as_view(),
        name="UploadFile"
        )
]
