from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os


# Load data
def data_load(data):
    loaded = DirectoryLoader(
        data, 
        glob="*.pdf",
        loader_cls=PyPDFLoader
        )
    return loaded.load()



def text_split(pdf_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
        )
    text_chunk = text_splitter.split_documents(pdf_data)
    return text_chunk


def huggingface_download():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

 