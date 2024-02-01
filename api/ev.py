import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

import time
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.vectorstores import Pinecone
from langchain_core.output_parsers import StrOutputParser
from pinecone import Pinecone as PC

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

from pathlib import Path
from django.conf import settings
from docs.models import DocumentModel

import json
import yaml


llm_template = """for the following question, just give me a very short answer.

Question: {question}
"""
llm_prompt = ChatPromptTemplate.from_template(llm_template)
llm_output_parser = StrOutputParser()
llm = ChatOpenAI(temperature= 0, model_name='gpt-3.5-turbo')
llm_chain = llm_prompt | llm | llm_output_parser

############# RAG #############
embeddings = OpenAIEmbeddings()

rag_template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

rag_prompt = ChatPromptTemplate.from_template(rag_template)

# initialize pinecone
pc = PC(
    api_key=settings.PINECONE_API_KEY,  # find at app.pinecone.io
    environment=settings.PINECONE_ENVIRONMENT,  # next to api key in console
)

index = pc.Index(settings.PINECONE_INDEX_NAME)
# vectorstore = Pinecone(index, embeddings.embed_query, "text", namespace=settings.PINECONE_NAMESPACE)
vectorstore = Pinecone(index, embeddings, "text", namespace=settings.PINECONE_NAMESPACE)

retriever = vectorstore.as_retriever()
# Read the JSON file
setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)

model = ChatOpenAI(temperature= 0, model_name='gpt-3.5-turbo')
output_parser = StrOutputParser()
rag_chain = setup_and_retrieval | rag_prompt | model | output_parser


results = []

with open('eval/test.json', 'r') as json_file:
    data = json.load(json_file)


    for i, d in enumerate(data[:200]):
        print("processing question", i)
        question = d["qText"]
        ans_list = d["answers"]

        llm_ans = llm_chain.invoke({"question": question})
        rag_ans = rag_chain.invoke(question)
        new_res = {
            "question": question,
            "llm": llm_ans,
            "rag": rag_ans,
            "answers": ans_list
        }
        results.append(new_res)
        time.sleep(0.2)

        with open('output.yaml', 'w') as yaml_file:
            yaml.dump(results, yaml_file, default_flow_style=False)