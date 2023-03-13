from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Document
from .forms import DocumentForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import ListView
# from .models import Document

from .AES import decrypt,getKey,decrypt_file


class DocumentListView(LoginRequiredMixin,ListView):
    login_url = '/accounts/login/'
    model = Document
    template_name = 'documents.html'
    context_object_name = 'documents'

class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'upload.html'
    success_url = reverse_lazy('home')
    
    def getInstance(self):
        return Document.objects.filter(user_id=self.request.user.id)    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.getInstance()
        print(context)
        user = self.request.user
        context["user"] = User.objects.get(id=user.id)
        return context
    def get_form_kwargs(self):
        kwargs = super(DocumentCreateView, self).get_form_kwargs()
        
        if kwargs['instance'] is None:
            kwargs['instance'] = Document()
        user = self.request.user
        user= User.objects.get(id=user.id)
        # form.instance.user = user
        kwargs['instance'].user = user
        print(kwargs)
        return kwargs
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     print("d----------------------------",dir(form))
    #     user = self.request.user
    #     user= User.objects.get(id=user.id)
    #     form.instance.user = user
    #     return super().form_valid(form)


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Document

def download(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    # decrypt(getKey(document.user.password),document.document.file.name)
    response = HttpResponse(document.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document.file.name}"'
    return response