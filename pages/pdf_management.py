from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
from simple_rag.crud.milvus_crud import get_unique_sources, add_documents
from simple_rag.services.embedding import google_model
from simple_rag.services.extract_pdf import pdf_extractor


def embedding_model() -> GoogleGenerativeAIEmbeddings:
    return google_model(
        google_api_key=st.secrets["google_api_key"],
        model_name="text-embedding-004",
    )


def on_data():
    st.session_state["datas"] = st.session_state["_datas"]


st.set_page_config(
    page_title="Simple RAG/PDF",
    page_icon=st.secrets["favicon"],
    layout="wide",
)

col1, col2, col3 = st.columns([0.3, 0.02, 0.68])

col1.header("데이터 추가")

col1.file_uploader(
    "파일 추가",
    key="_datas",
    label_visibility="collapsed",
    type="pdf",
    accept_multiple_files=True,
    on_change=on_data,
)


#
col3.header("상태")
co1, co2, co3 = col3.columns(3)

co1.subheader("완료")
ready = co1.empty()

co2.subheader("대기중")
wait = co2.empty()


co3.subheader("처리중")
field_ing = co3.empty()


if "datas" in st.session_state:
    for data in st.session_state["datas"]:
        try:
            db_data = get_unique_sources(
                zilliz_uri=st.secrets["milvus_uri"],
                zilliz_token=st.secrets["milvus_token"],
            )

            ready_field = ready.container()
            for data1 in db_data:
                ready_field.info(data1)
        except:
            pass

        st.session_state["datas"].pop(0)
        field_ing.success(data.name)

        wait_field = wait.container()
        for i in st.session_state["datas"]:
            wait_field.warning(i.name)

        with open("dummy.pdf", mode="wb") as w:
            w.write(data.getvalue())

        docs = pdf_extractor(path="dummy.pdf")
        add_documents(
            embedding_model=embedding_model(),
            zilliz_uri=st.secrets["milvus_uri"],
            zilliz_token=st.secrets["milvus_token"],
            documents=docs,
        )
        if st.session_state["datas"]:
            ready.empty()
            wait.empty()

field_ing.empty()
try:
    db_data = get_unique_sources(
        zilliz_uri=st.secrets["milvus_uri"],
        zilliz_token=st.secrets["milvus_token"],
    )

    field_ready = ready.container()
    for data in db_data:
        field_ready.info(data)
except:
    pass
