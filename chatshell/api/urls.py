from django.urls import path
from chatshell.api.views import AskQueryView

urlpatterns = [
    path("ask/",AskQueryView.as_view(),name="ask-question"),
]
