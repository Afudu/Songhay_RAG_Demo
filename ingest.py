# ingest.py

"""Ingests glossary data from an Excel file,
generates embeddings using Azure OpenAI,
and stores them in a PostgreSQL vector database."""

from app import load_excel_as_documents, GLOSSARY_DATA_PATH, PG_CONNECTION_STRING
from app import AZURE_EMBEDDING_DEPLOYMENT, AZURE_OPENAI_ENDPOINT
from app import AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, COLLECTION_NAME
from langchain_openai import AzureOpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

documents = load_excel_as_documents(GLOSSARY_DATA_PATH)
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
chunks = splitter.split_documents(documents)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
)

PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection=PG_CONNECTION_STRING,
    pre_delete_collection=True,  # always wipes and re-ingests
)

print("Ingestion complete.")
