import streamlit as st

def make_camera_controls():
    col1, col2, col3 = st.columns(3)
    with col1:
        axis1 = st.number_input("axis1",step=.1,value=1.0)
    with col2:
        axis2 = st.number_input("axis2",step=.1,value=-1.0)
    with col3:
        axis3 = st.number_input("axis3",step=.1, value=-0.5)

    focus = st.number_input("Focus",step=1, value=50)
    return {
        'axis1':axis1, 
        'axis2':axis2, 
        'axis3':axis3, 
        'focus':focus
    }