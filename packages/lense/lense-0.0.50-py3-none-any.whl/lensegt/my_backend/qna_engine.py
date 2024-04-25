from langchain_community.llms import HuggingFaceHub

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import re
import os
import openai
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
import warnings
warnings.filterwarnings('ignore')


def embed_and_run_mistral(documents,hf_token=None):
    pattern = r"Answer: (.*)"
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceHub(huggingfacehub_api_token=hf_token,
                        repo_id=repo_id, model_kwargs={"temperature":0.5, "max_new_tokens":100})

    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    index = VectorStoreIndex.from_documents(documents, embed_model = embed_model, show_progress=True)
    query_engine = index.as_query_engine(similarity_top_k=3,llm=llm)

    return query_engine.query

def embed_and_run_openai(documents,api_key=None):


    os.environ["OPENAI_API_KEY"] = api_key
    openai.api_key = os.environ["OPENAI_API_KEY"]
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    llm = OpenAI(model="gpt-3.5-turbo")
    query_engine = index.as_query_engine(similarity_top_k=3,llm=llm)
    
    return query_engine.query

def embed_and_run_azureopenai(documents,api_key=None,api_version=None,azure_endpoint=None):
    


    api_key= api_key 
    api_version=api_version
    azure_endpoint=azure_endpoint
    

    llm = AzureOpenAI(
        model="gpt-35-turbo-16k",
        deployment_name="gpt-35-turbo-16k",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
        max_tokens=50,
    )

    # You need to deploy your own embedding model as well as your own chat completion model
    embed_model = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name="text-embedding-ada-002",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

    
    Settings.llm = llm
    Settings.embed_model = embed_model

    index = VectorStoreIndex.from_documents(documents, show_progress=True)#, embed_model = embed_model, show_progress=True,)
    query_engine = index.as_query_engine(similarity_top_k=3,llm=llm)
    
    return query_engine.query


