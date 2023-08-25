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