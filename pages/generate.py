import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from simple_rag.database.milvus import milvus
from simple_rag.services.embedding import google_model


st.set_page_config(
    page_title="Simple RAG/Chat",
    page_icon=st.secrets["favicon"],
    layout="wide",
)


embedding_model = google_model(
    google_api_key=st.secrets["google_api_key"],
    model_name="text-embedding-004",
)
vector_db = milvus(
    embedding_model=embedding_model,
    zilliz_uri=st.secrets["milvus_uri"],
    zilliz_token=st.secrets["milvus_token"],
)

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful assistant that Explane **Document** If the answer is not found in the documentation, print “주어진 문서에서 확인할 수 없습니다.” ",
        ),
        ("user", "**Document:**\n\n{documents}"),
        ("user", "{question}"),
    ]
)
# background.set_img(st.secrets["background_img2"])
# LLM 불러오기 "Gemini-1.5-flash" 사용
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # 사용할 LLM
    api_key=st.secrets["google_api_key"],  # Google API-KEY
)
chain = (
    {
        "documents": vector_db.as_retriever(
            search_kwargs={
                "k": 10,
                "score_threshold": 0.6,
            }
        ),
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)
col1, col2, col3 = st.columns(3)

main = col2.container(height=600)
if col2.chat_input(key="user_input"):
    with main.chat_message("user"):
        st.markdown(st.session_state["user_input"])

    with main.chat_message("ai"):
        st.write_stream(chain.stream(st.session_state["user_input"]))
