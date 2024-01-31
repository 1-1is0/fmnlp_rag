from django.shortcuts import render
from rest_framework import viewsets
from docs.models import DocumentModel
from docs.serializers import DocumentSerializer

# Create your views here.

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = DocumentModel.objects.all()
    serializer_class = DocumentSerializer