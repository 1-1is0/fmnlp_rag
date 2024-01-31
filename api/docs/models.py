from django.db import models

# Create your models here.

class DocumentModel(models.Model):
    name = models.CharField(max_length=255)
    docfile = models.FileField(upload_to='documents/')