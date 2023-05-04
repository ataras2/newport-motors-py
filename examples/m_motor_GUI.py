import streamlit as st
import pandas as pd
import numpy as np

from newport_motors.GUI.CustomNumeric import CustomNumeric
from newport_motors.GUI.InstrumentGUI import InstrumentGUI
from newport_motors.Motors.motor import M100D


# TODO: make min, max, step consistent and easy to interface
# TODO: Add axes labels, titles
# TODO: add tip/tilt scatter with colours going backwards in time


st.set_page_config(layout="wide")

st.title('Motor control for Heimdallr')

# # error here, on change uses the previous value of component or beam 
# # i.e. the call back occurs before beam assignment...
# def on_item_change():
#    print(f"Changing internals to {component}{beam}")

if 'motor' not in st.session_state:
    import pyvisa
    st.session_state['motor'] = M100D('ASRL/dev/ttyUSB0::INSTR', pyvisa.ResourceManager())


col1, col2 = st.columns(2)

with col1:
    component = st.selectbox("Pick a component", ["OAP1","Spherical mirror","Knife edge"], key="component")

with col2:
    beam = st.selectbox("Pick a component", list(range(1,5)), key="beam")


st.write(f"Currently looking at {component}, beam {beam}")


col1, col2 = st.columns(2)

with col1:
    st.header("Linear motor")
    def update_slider():
        st.session_state.slider = st.session_state.numeric
    def update_numin():
        st.session_state.numeric = st.session_state.slider            



    ccol1, ccol2 = st.columns(2)
    with ccol1:
        val = st.number_input('Displacement (mm)', value = 0, key = 'numeric', on_change = update_slider)

    with ccol2:
        slider_value = st.slider('slider', min_value = 0, 
                            value = val, 
                            max_value = 5,
                            step = 1,
                            key = 'slider', on_change= update_numin)
    
    st.line_chart(np.random.randn(20, 1))
#    component = st.selectbox("Pick a component", ["OAP1","Spherical mirror"])


def TipTiltMotor():
    st.header("Tip/Tilt motor")
    CustomNumeric.variable_increment('x',InstrumentGUI.get_update_fn('x'))
    

with col2:
    TipTiltMotor()
#    beam = st.selectbox("Pick a component", list(range(1,5)))



