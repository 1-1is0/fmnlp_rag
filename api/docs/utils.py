from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from django.conf import settings
import pinecone

def proccess_document(pdf_dir):
    loader = PyPDFLoader("example_data/layout-parser-paper.pdf", extract_images=True)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    docs = text_splitter.split_documents(pages)
    embeddings = OpenAIEmbeddings()


    # initialize pinecone
    pinecone.init(
        api_key=settings.PINECONE_API_KEY,  # find at app.pinecone.io
        environment=settings.PINECONE_ENVIRONMENT,  # next to api key in console
    )

    index = pinecone.Index(settings.PINECONE_INDEX_NAME)
    vectorstore = Pinecone(index, embeddings.embed_query, "text")
    vectorstore.add_documents(docs)

    # docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)