import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_milvus import Milvus


def embedding_model() -> GoogleGenerativeAIEmbeddings:
    """Google의 Embedding 모델을 불러오는 함수

    Returns
    -------
    GoogleGenerativeAIEmbeddings
        불러온 Embedding 모델

    Model list
    ----------
    - "models/embedding-001"
    -
    """
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=st.secrets["api_key"],
    )


def milvus_client() -> Milvus:
    return Milvus(
        embedding_function=embedding_model(),
        collection_name=st.secrets["collection_name"],
        connection_args={
            "uri": st.secrets["milvus_uri"],
            "token": st.secrets["milvus_token"],
        },
        auto_id=True,
    )


def pdf_extractor(path):
    pages = []
    for page in PyPDFLoader(file_path=path).load():
        pages.append(page)
    return pages


def add_pdf(byte_file):
    vector_db = milvus_client()
    with open(byte_file.name, mode="wb") as w:
        w.write(byte_file.getvalue())
    vector_db.add_documents(documents=pdf_extractor(byte_file.name))
