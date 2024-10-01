from time import sleep
import streamlit as st
from functions import add_pdf, available_document, chat_bot

title = "Simple RAG"

# Page 기본값 설정
st.set_page_config(page_title=title, page_icon=st.secrets["favicon"], layout="wide")
if "select" in st.session_state:
    prompt = st.secrets[f"prompt{st.session_state['select']}"]
else:
    prompt = st.secrets["prompt1"]
if "available_document" not in st.session_state:
    st.session_state["available_document"] = available_document()
st.header(f"🤖 {title}")
st.divider()

left, right = st.columns(spec=[0.4, 0.6], gap="large")

# 왼쪽
left.subheader("🗃️ Data")
with left.form("my-form", clear_on_submit=True, border=False):
    files = st.file_uploader("_", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
    submitted = st.form_submit_button("submit", use_container_width=True)
    field = st.empty()
    if submitted:
        for data in files:
            field.warning(data.name)
            add_pdf(data)
            field.success(data.name)
            sleep(0.5)
        field.empty()
        st.session_state["available_document"] = available_document()
docs_name = left.multiselect("**사용 가능한 문서**", key="select_document", options=st.session_state["available_document"])
left.divider()
left.subheader("📝 System Prompt")
system_prompt = left.text_area("_", key="prompt", value=prompt, label_visibility="collapsed", height=240)

# 오른쪽
right.subheader("🗪 Chat")
chat_field = right.container(height=600, border=True)
select_title, select_field, input_field = right.columns([0.06, 0.15, 0.79])
select_title.markdown("**MODE:** ")
select_field.radio("_", [1, 2, 3], key="select", horizontal=True, label_visibility="collapsed")
if input_field.chat_input(key="user_input"):
    with chat_field.chat_message("human"):
        st.text(st.session_state["user_input"])
    with chat_field.chat_message("ai"):
        with st.spinner("생각하는 중..."):
            st.write_stream(chat_bot(system_prompt=system_prompt, use_docs=docs_name))
