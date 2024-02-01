from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from docs.models import DocumentModel, DocumentIds
