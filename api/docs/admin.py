from django.contrib import admin
from docs.models import DocumentModel, DocumentIds

# Register your models here.

admin.site.register(DocumentModel)
admin.site.register(DocumentIds)