from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as PC

from pathlib import Path
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

# Create your models here.

class DocumentModel(models.Model):
    name = models.CharField(max_length=255)
    docfile = models.FileField(upload_to='documents/')
    proccsed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.name}"

class DocumentIds(models.Model):
    doc = models.ForeignKey(DocumentModel, on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.doc} - {self.ref_id}"

@receiver(post_save, sender=DocumentModel)
def process_document_model(sender, instance, created, **kwargs):
    if created and not instance.proccsed:
        proccess_document(instance)
        instance.proccsed = True
        instance.save()

@receiver(pre_delete, sender=DocumentModel)
def delete_document_model(sender, instance, **kwargs):
    delete_doc_from_pinecore(instance)

def proccess_document(doc_model: DocumentModel):

    media_base = Path(settings.MEDIA_ROOT)
    doc_dir = media_base / doc_model.docfile.name
    # loader = PyPDFLoader(doc_dir.as_posix(), extract_images=True)
    loader = PyPDFLoader(doc_dir.as_posix())
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    docs = text_splitter.split_documents(pages)
    embeddings = OpenAIEmbeddings()


    # initialize pinecone
    pc = PC(
        api_key=settings.PINECONE_API_KEY,  # find at app.pinecone.io
        environment=settings.PINECONE_ENVIRONMENT,  # next to api key in console
    )

    index = pc.Index(settings.PINECONE_INDEX_NAME)
    # vectorstore = Pinecone(index, embeddings.embed_query, "text", namespace=settings.PINECONE_NAMESPACE)
    vectorstore = Pinecone(index, embeddings, "text", namespace=settings.PINECONE_NAMESPACE)
    res = vectorstore.add_documents(docs)
    print("res", res)
    for res_id in res:
        d = DocumentIds.objects.create(doc=doc_model, ref_id=res_id)
        print("created document id", d.ref_id)

def delete_doc_from_pinecore(doc_model: DocumentModel):
    pc = PC(
        api_key=settings.PINECONE_API_KEY,  # find at app.pinecone.io
        environment=settings.PINECONE_ENVIRONMENT,  # next to api key in console
    )
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    document_ids = DocumentIds.objects.filter(doc=doc_model)
    for doc_id in document_ids:
        print("delete", doc_id.doc, "ref", doc_id.ref_id)
        index.delete(ids=[doc_id.ref_id], namespace=settings.PINECONE_NAMESPACE)
