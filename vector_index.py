from resource.helper import data_load, text_split, huggingface_download
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os
from langchain_pinecone import PineconeVectorStore

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")


pdf_data = data_load('Data\\')
text_chunk = text_split(pdf_data=pdf_data)
embeddings = huggingface_download()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "med-bot"

pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
    
)

med_db = PineconeVectorStore.from_documents(
    documents=text_chunk,
    index_name=index_name,
    embedding=embeddings
)