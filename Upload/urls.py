from django.urls import path
from .views import DocumentCreateView, DocumentListView, download
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', DocumentListView.as_view(), name='home'),
    path('upload/', login_required(DocumentCreateView.as_view()), name='upload'),
    path('download/<int:document_id>/', login_required(download), name='download'),
]