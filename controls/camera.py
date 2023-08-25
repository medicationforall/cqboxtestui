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