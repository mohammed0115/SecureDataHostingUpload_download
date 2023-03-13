from django import forms
from .models import Document
from django.contrib.auth.models import User
class DocumentForm(forms.ModelForm):
    # user = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden','value':}))
    class Meta:
        model = Document
        fields = ('description', 'document')
