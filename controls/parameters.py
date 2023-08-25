import streamlit as st

def make_parameter_controls():
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Length",min_value=1,value=10)
    with col2:
        width = st.number_input("Width",min_value=1,value=30)
    with col3:
        height = st.number_input("height",min_value=1, value=10)

    return {
        'length':length,
        'width':width,
        'height':height
    }