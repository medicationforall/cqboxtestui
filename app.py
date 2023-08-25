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
import cadquery as cq
import os
import time


EXPORT_NAME = 'model'
PREVIEW_NAME = 'preview.svg'

def __generate_model(parameters):
    model = (
        cq.Workplane("XY")
        .box(
            parameters['length'],
            parameters['width'],
            parameters['height']
        )
    )
    return model

def __generate_preview_image(model, image_name, color1, color2, camera):
    #create the preview image
    hex_1 = color1.lstrip('#')
    rgb_1 = tuple(int(hex_1[i:i+2], 16) for i in (0, 2, 4))

    hex_2 = color2.lstrip('#')
    rgb_2 = tuple(int(hex_2[i:i+2], 16) for i in (0, 2, 4))
    cq.exporters.export(model, image_name, opt={
        "projectionDir": (camera['axis1'], camera['axis2'], camera['axis3']),
        "showAxes": True,
        "focus": camera['focus'],
        "strokeColor": rgb_1,
        "hiddenColor": rgb_2
    })


def make_model_controls(
    parameters,
    camera,
    color1, 
    color2, 
    file_controls
):
    start = time.time()
    with st.spinner('Generating Model..'):
        download_name = file_controls['name']
        export_type = file_controls['type'] 
        model = __generate_model(parameters)

        #create the model file for downloading
        cq.exporters.export(model,f'{EXPORT_NAME}.{export_type}')
        __generate_preview_image(model, PREVIEW_NAME, color1, color2, camera)

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

#--------------------

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

#--------------------

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

#--------------------

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

#--------------------

def make_sidebar():
    with st.sidebar:
        st.markdown("![](https://miniforall.com/image/patreon.png) [Patreon](https://www.patreon.com/medicationforall)")
        st.markdown("[Mini For All](https://miniforall.com)")
        st.markdown("[Github Code](https://github.com/medicationforall/cqboxtestui)")

#--------------------

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