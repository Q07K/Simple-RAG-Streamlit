import streamlit as st


def set_img(img_url):
    background_image = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("{img_url}");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}}
</style>
"""
    # Display the background image
    st.markdown(background_image, unsafe_allow_html=True)
