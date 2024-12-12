import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core import prompts, output_parsers, runnables
from langchain_milvus import Milvus


def embedding():
    return GoogleGenerativeAIEmbeddings(
        model=f"models/{st.secrets['embedded']}",
        google_api_key=st.secrets["api_key"],
    )


def milvus():
    return Milvus(
        embedding_function=embedding(),
        collection_name=st.secrets["collection_name"],
        connection_args={
            "uri": st.secrets["milvus_uri"],
            "token": st.secrets["milvus_token"],
        },
        auto_id=True,
    )


def chat_bot(system_prompt, use_docs):
    vector_db = milvus()
    prompt = prompts.ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("user", f"**Document List:**{use_docs}"),
            ("user", "**Document:**\n\n{context}"),
            ("user", "{question}"),
        ]
    )
    llm = ChatGoogleGenerativeAI(
        model=st.secrets["model"],
        api_key=st.secrets["api_key"],
    )
    context = vector_db.as_retriever(
        search_kwargs={
            "k": 10,
            "score_threshold": 0.3,
            "expr": f"source in {list(use_docs)}",
        }
    )
    chain = {"context": context, "question": runnables.RunnablePassthrough()} | prompt | llm | output_parsers.StrOutputParser()
    return chain.stream(st.session_state["user_input"])
