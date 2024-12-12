import streamlit as st

from functions import add_pdf

TITLE = "Simple RAG"

# Page 기본값 설정
st.set_page_config(page_title=TITLE)

# Page Title
st.header(f"🤖 {TITLE}")
st.divider()

# Content
st.subheader("🗃️ Data")
with st.form("my-form", clear_on_submit=True, border=False):
    files = st.file_uploader(
        "_",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button(
        "submit",
        use_container_width=True,
    )
    field = st.empty()
    if submitted:
        for data in files:
            add_pdf(data)
