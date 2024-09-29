import streamlit as st
from simple_rag.streamlit_controllers import background

st.set_page_config(
    page_title="Simple RAG",
    page_icon=st.secrets["favicon"],
    layout="wide",
)


background.set_img(st.secrets["background_img1"])
a = st.warning("")
a.text_input("s")
