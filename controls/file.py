import streamlit as st

def make_file_controls():
    col1, col2 = st.columns(2)
    with col1:
        download_name = st.text_input('File Name','model')
    with col2:
        export_type = st.selectbox("File type",('stl','step'))
    return {
        'name':download_name,
        'type':export_type
    }