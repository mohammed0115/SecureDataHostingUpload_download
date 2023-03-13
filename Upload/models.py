from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from .AES import encrypt,getKey,encrypt_file
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document    = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey(User, verbose_name="User",null=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        print("file name:",(self.document.file.name))
       
        super(Document, self).save(*args, **kwargs)
        self.document = open(encrypt(getKey(self.user.password), self.document.file.name))