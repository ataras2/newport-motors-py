import streamlit as st
import pandas as pd
import numpy as np

from newport_motors.GUI.CustomNumeric import CustomNumeric
from newport_motors.GUI.InstrumentGUI import InstrumentGUI
from newport_motors.Motors.motor import M100D
import pyvisa

# TODO: have persistence when dropdowns are changed
# TODO: Add axes labels, titles
# TODO: add tip/tilt scatter with colours going backwards in time

import logging

logging.basicConfig(filename='example.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format='%(filename)s:%(levelname)s:%(message)s')

run_in_sim = True



st.set_page_config(layout="wide")

st.title('Motor control for Heimdallr')


if 'motor1' not in st.session_state:
    if run_in_sim:
        from newport_motors.Mocks.motor import Mock_M100D
        from visa_mock.base.register import register_resource

        motor1_port = 'MOCK0::mock1::INSTR'
        motor2_port = 'MOCK0::mock2::INSTR'

        register_resource(motor1_port, Mock_M100D())
        register_resource(motor2_port, Mock_M100D())

        rm = pyvisa.ResourceManager(visa_library="@-mock")
    else:
        motor1_port = 'ASRL/dev/ttyUSB0::INSTR'
        motor2_port = 'ASRL/dev/ttyUSB1::INSTR'
        rm = pyvisa.ResourceManager(visa_library="@-py")


    st.session_state['motor1'] = M100D(motor1_port, rm)
    st.session_state['motor2'] = M100D(motor2_port, rm)

st.session_state['motor1'].set_absolute_position(0.02, M100D.AXES.U)

col1, col2 = st.columns(2)

with col1:
    component = st.selectbox("Pick a component", ["OAP1","Spherical mirror","Knife edge"], key="component")

with col2:
    beam = st.selectbox("Pick a component", list(range(1,5)), key="beam")


st.write(f"Currently looking at {component}, beam {beam}")

if beam > 1:
    motor_key = 'motor2'
else:
    motor_key = 'motor1'


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
    
    # st.line_chart(np.random.randn(20, 1))
#    component = st.selectbox("Pick a component", ["OAP1","Spherical mirror"])


def TipTiltMotor():
    st.header("Tip/Tilt motor")
    CustomNumeric.variable_increment(['x', 'y'],
                                     [InstrumentGUI.get_update_fn('x', motor_key), InstrumentGUI.get_update_fn('y', motor_key)],
                                     st.session_state[motor_key].get_current_pos())
    pos = st.session_state[motor_key].get_current_pos()

    import plotly.express as px

    fig = px.scatter(
        x=np.array([pos[0]]),
        y=np.array([pos[1]]),
    )
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        yaxis = dict(range=st.session_state[motor_key].HW_BOUNDS[M100D.AXES.V]),
        xaxis = dict(range=st.session_state[motor_key].HW_BOUNDS[M100D.AXES.U])
    )

    st.write(fig)


with col2:
    TipTiltMotor()
#    beam = st.selectbox("Pick a component", list(range(1,5)))



