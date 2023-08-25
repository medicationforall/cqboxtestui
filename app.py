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
import base64

def __render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

def __model(length, width, height,axis1,axis2,axis3, focus, color1, color2):
    start = time.time()
    with st.spinner('Wait for it...'):
        box = cq.Workplane("XY").box(length,width,height)
        cq.exporters.export(box,"test.stl")

        hex_1 = color1.lstrip('#')
        rgb_1 = tuple(int(hex_1[i:i+2], 16) for i in (0, 2, 4))

        hex_2 = color2.lstrip('#')
        rgb_2 = tuple(int(hex_2[i:i+2], 16) for i in (0, 2, 4))
        cq.exporters.export(box, "box.svg", opt={
            "projectionDir": (axis1, axis2, axis3),
            "showAxes": True,
            "focus": focus,
            "strokeColor": rgb_1,
            "hiddenColor": rgb_2
        })

        end = time.time()

        st.write("Preview:")
        with open('box.svg', 'r') as f:
            __render_svg(f.read())

        if f'test.stl' not in os.listdir():
            st.error('The program was not able to generate the mesh.', icon="🚨")
        else:
            with open('test.stl', "rb") as file:
                btn = st.download_button(
                        label=f"Download STL",
                        data=file,
                        file_name=f'test.stl',
                        mime=f"model/stl"
                    )
            st.success(f'Rendered in {int(end-start)} seconds', icon="✅")


def __make_ui():
    tab1, tab2 = st.tabs(["Parameters", "Camera"])

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

    col1, col2, col3= st.columns(3)
    with col1:
        render = st.checkbox('Render:', True)
    with col2:
        color1 = st.color_picker('Primary Color', '#00f900', disabled=not render)
    with col3:
        color2 = st.color_picker('Secondary Color', '#0011f9', disabled=not render)

    if render:
        __model(length, width, height,axis1,axis2,axis3, focus, color1, color2)

def __make_sidebar():
    with st.sidebar:
        st.markdown("![](https://miniforall.com/image/patreon.png) [Patreon](https://www.patreon.com/medicationforall)")
        st.markdown("[Mini For All](https://miniforall.com)")
        st.markdown("[Github Code](https://github.com/medicationforall/cqboxtestui)")


if __name__ == "__main__":
    st.set_page_config(
    page_title="CadQuery Box Test",
    page_icon="🧊"
    )

    st.title('CadQuery Box Test')
    __make_ui()
    __make_sidebar()