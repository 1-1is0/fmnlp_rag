from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from docs.utils import process_document

# Create your models here.

class DocumentModel(models.Model):
    name = models.CharField(max_length=255)
    docfile = models.FileField(upload_to='documents/')
    proccsed = models.BooleanField(default=False)

@receiver(post_save, sender=DocumentModel)
def process_document_model(sender, instance, created, **kwargs):
    if created and not instance.proccsed:
        process_document(instance.docfile.path)
        instance.proccsed = True
        instance.save()