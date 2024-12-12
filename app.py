import streamlit as st
from functions import chat_bot

title = "Simple RAG"

# Page 기본값 설정
st.set_page_config(page_title=title)
st.header(f"🤖 {title}")
st.divider()

st.subheader("🗪 Chat")
chat_field = st.container(height=600, border=True)
if st.chat_input(key="user_input"):
    with chat_field.chat_message("human"):
        st.markdown(st.session_state["user_input"])
    with chat_field.chat_message("ai"):
        with st.spinner("생각하는 중..."):
            st.write_stream(chat_bot(system_prompt="system_prompt"))
