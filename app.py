"""
RAG Demo — Songhay IT Glossary
Trilingual IT terminology (English / French / Songhay)
"""

import pandas as pd
import streamlit as st
from decouple import config
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_postgres.vectorstores import PGVector
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# ── Configuration ─────────────────────────────────────────────────────────────
AZURE_OPENAI_API_KEY = config("AZURE_OPENAI_API_KEY", default="")
AZURE_OPENAI_ENDPOINT = config("AZURE_OPENAI_ENDPOINT", default="", cast=str)
AZURE_OPENAI_API_VERSION = config("AZURE_OPENAI_API_VERSION", default="2024-02-01")
AZURE_DEPLOYMENT_NAME = config("AZURE_DEPLOYMENT_NAME", default="gpt-4o")
AZURE_EMBEDDING_DEPLOYMENT = config("AZURE_EMBEDDING_DEPLOYMENT", default="text-embedding-ada-002")
PG_CONNECTION_STRING = config("PG_CONNECTION_STRING", default="")
GLOSSARY_DATA_PATH = config("GLOSSARY_DATA_PATH", default="songhay_it_glossary.xlsx")

COLLECTION_NAME = "songhay_it_glossary"

# Prompt template for the RAG chain.
PROMPT_TEMPLATE = """
You are a helpful assistant for a trilingual IT glossary (English, French, Songhay).
Use ONLY the context below to answer. If the term is not in the glossary, say so clearly.
Always show all three languages when available: English, French, and Songhay.

Context:
{context}

Question: {input}

Answer:
"""


# ── Data Loader ─────────────────────────────────────────────────────────────

def is_empty(val: str) -> bool:
    """Returns True if a cell is blank or pandas NaN-as-string."""
    return not val or val.lower() == "nan"


def load_excel_as_documents(path: str) -> list[Document]:
    """
    Reads the Excel glossary and converts each row into a LangChain Document.
    Expects headers: English, French, Songhay
    Each row becomes one document: one entry, one chunk, clean retrieval.
    """
    df = pd.read_excel(path, engine="openpyxl")

    if df.empty:
        return []

    df.columns = df.columns.str.strip()

    documents = []
    for _, row in df.iterrows():
        en = str(row.get("English", "")).strip()
        fr = str(row.get("French", "")).strip()
        so = str(row.get("Songhay", "")).strip()

        if is_empty(en) or en.lower() == "english":
            continue
        if is_empty(fr) or fr.lower() == "french":
            continue
        if is_empty(so) or so.lower() == "songhay":
            continue

        content = f"English: {en}\nFrench: {fr}\nSonghay: {so}"
        documents.append(Document(
            page_content=content,
            metadata={"english": en, "french": fr, "songhay": so},
        ))

    return documents


# ── Vectorstore (cached — only indexes once per session) ──────────────────────

@st.cache_resource(show_spinner="Indexing glossary into pgvector...")
def load_vectorstore():
    """Loads the Excel glossary, converts to Documents, embeds, and stores in pgvector.
    Cached for efficiency."""

    # 1- Load Excel and convert to LangChain Documents
    documents = load_excel_as_documents(GLOSSARY_DATA_PATH)

    # 2- Entries are already short — splitter is a safety net only
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(documents)

    # 3- Embed using Azure OpenAI
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    # 4 - Store in pgvector (creates collection if it doesn't exist, or reuses if it does)
    vectorstore = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=PG_CONNECTION_STRING,
        pre_delete_collection=False,  # set True to force re-index
    )
    return vectorstore


# ── RAG Chain ─────────────────────────────────────────────────────────────────

def build_qa_chain(vectorstore):
    llm = AzureChatOpenAI(
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        temperature=0,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "input"],
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    return chain


# ── Streamlit UI ───────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="Songhay IT Glossary",
                       page_icon="img/son_favicon.ico", layout="centered")

    st.title("Songhay IT Glossary — RAG Demo")
    st.caption("Trilingual IT terminology: English · French · Songhay")
    st.divider()

    vectorstore = load_vectorstore()
    qa_chain = build_qa_chain(vectorstore)

    st.markdown("**Try asking:**")
    examples = [
        "What is the Songhay word for 'database'?",
        "How do you say 'open' in French and Songhay?",
        "What does 'Tataaru-hugu' mean?",
        "Give me all terms related to security",
        "What is the Songhay translation for 'password'?",
        "What is the Songhay translation for 'certificate'?",
    ]
    # Display example buttons in two columns
    cols = st.columns(2)

    # Loop through examples and assign them to columns alternately
    for i, ex in enumerate(examples):
        if cols[i % 2].button(ex, use_container_width=True):
            st.session_state["query"] = ex

    st.divider()

    # Input box for user query (pre-filled if an example button was clicked)
    query = st.text_input(
        "Ask anything about the glossary:",
        value=st.session_state.get("query", ""),
        placeholder="e.g. What is 'firewall' in Songhay?",
    )

    if query:
        with st.spinner("Searching glossary..."):
            answer = qa_chain.invoke(query)

        st.markdown("### Answer")
        st.success(answer)

        with st.expander("Source entries used"):
            # Number of source documents to retrieve (k=5 here)
            docs = vectorstore.as_retriever(search_kwargs={"k": 5}).invoke(query)
            for doc in docs:
                st.text(doc.page_content)


if __name__ == "__main__":
    main()
