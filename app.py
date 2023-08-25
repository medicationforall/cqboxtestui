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

import streamlit as st
import cadquery as cq
import os
import time
from sidebar import sidebar

EXPORT_NAME = 'model'
PREVIEW_NAME = 'preview.svg'

def __model(
    length, 
    width, 
    height,
    axis1,
    axis2,
    axis3, 
    focus, 
    color1, 
    color2, 
    download_name, 
    export_type
):
    start = time.time()
    with st.spinner('generating model..'):
        box = cq.Workplane("XY").box(length,width,height)
        cq.exporters.export(box,f'{EXPORT_NAME}.{export_type}')

        hex_1 = color1.lstrip('#')
        rgb_1 = tuple(int(hex_1[i:i+2], 16) for i in (0, 2, 4))

        hex_2 = color2.lstrip('#')
        rgb_2 = tuple(int(hex_2[i:i+2], 16) for i in (0, 2, 4))
        cq.exporters.export(box, PREVIEW_NAME, opt={
            "projectionDir": (axis1, axis2, axis3),
            "showAxes": True,
            "focus": focus,
            "strokeColor": rgb_1,
            "hiddenColor": rgb_2
        })

        end = time.time()

        st.write("Preview:")
        st.image(PREVIEW_NAME)


        if f'{EXPORT_NAME}.{export_type}' not in os.listdir():
            st.error('The program was not able to generate the mesh.', icon="🚨")
        else:
            with open(f'{EXPORT_NAME}.{export_type}', "rb") as file:
                btn = st.download_button(
                        label=f"Download {export_type}",
                        data=file,
                        file_name=f'{download_name}.{export_type}',
                        mime=f"model/{export_type}"
                    )
            st.success(f'Rendered in {int(end-start)} seconds', icon="✅")


def __make_ui():
    tab1, tab2, tab3 = st.tabs(["Parameters", "Camera", "Meta"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            length = st.number_input("Length",min_value=1,value=10)
        with col2:
            width = st.number_input("Width",min_value=1,value=30)
        with col3:
            height = st.number_input("height",min_value=1, value=10)

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            axis1 = st.number_input("axis1",step=.1,value=1.0)
        with col2:
            axis2 = st.number_input("axis2",step=.1,value=-1.0)
        with col3:
            axis3 = st.number_input("axis3",step=.1, value=-0.5)

        focus = st.number_input("Focus",step=1, value=50)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            download_name = st.text_input('File Name','model')
        with col2:
            export_type = st.selectbox("File type",('stl','step'))

    col1, col2, col3= st.columns(3)
    with col1:
        render = st.checkbox('Render:', True)
    with col2:
        color1 = st.color_picker('Primary Color', '#00f900', disabled=not render)
    with col3:
        color2 = st.color_picker('Secondary Color', '#0011f9', disabled=not render)

    if render:
        __model(length, width, height,axis1,axis2,axis3, focus, color1, color2, download_name, export_type)


if __name__ == "__main__":
    st.set_page_config(
    page_title="CadQuery Box Test",
    page_icon="🧊"
    )

    st.title('CadQuery Box Test')
    __make_ui()
    sidebar()