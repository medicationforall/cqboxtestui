# Copyright 2023 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#--------------------  

import streamlit as st
from  controls import (
    make_sidebar, 
    make_parameter_controls, 
    make_model_controls,
    make_file_controls,
    make_camera_controls
)

def __make_ui():
    tab1, tab2, tab3 = st.tabs(["Parameters", "Camera", "File"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        model_parameters = make_parameter_controls()
    with tab2:
        camera_controls = make_camera_controls()
    with tab3:
        file_controls = make_file_controls()

    col1, col2, col3= st.columns(3)
    with col1:
        render = st.checkbox('Render:', True)
    with col2:
        color1 = st.color_picker('Primary Color', '#00f900', disabled=not render)
    with col3:
        color2 = st.color_picker('Secondary Color', '#0011f9', disabled=not render)

    if render:
        make_model_controls(
            model_parameters, 
            camera_controls, 
            color1, 
            color2, 
            file_controls
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="CadQuery Box Test",
        page_icon="🧊"
    )

    st.title('CadQuery Box Test')
    __make_ui()
    make_sidebar()