import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core import prompts, output_parsers, runnables
from langchain_milvus import Zilliz

PROMPT_TEMPLATE = """
Human: You are an AI assistant, and provides answers to questions by using fact based and statistical information when possible.
Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

<question>
{question}
</question>

The response should be specific and use statistics or numbers when possible.

Assistant:"""


def embedding():
    return GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=st.secrets["api_key"],
    )


def zilliz_client():
    return Zilliz(
        embedding_function=embedding(),
        collection_name=st.secrets["collection_name"],
        connection_args={
            "uri": st.secrets["milvus_uri"],
            "token": st.secrets["milvus_token"],
        },
        auto_id=True,
    )


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def generate(user_input):
    vector_db = zilliz_client()
    prompt = prompts.PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )
    llm = ChatGoogleGenerativeAI(
        model=st.secrets["model"],
        api_key=st.secrets["api_key"],
    )
    retriever = vector_db.as_retriever()
    chain = (
        {
            "context": retriever | format_docs,
            "question": runnables.RunnablePassthrough(),
        }
        | prompt
        | llm
        | output_parsers.StrOutputParser()
    )
    return chain.stream(user_input)
