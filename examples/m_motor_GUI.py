import streamlit as st
import pandas as pd
import numpy as np

from newport_motors.GUI.CustomNumeric import CustomNumeric
from newport_motors.GUI.InstrumentGUI import InstrumentGUI
from newport_motors.Motors.motor import M100D


# TODO: have persistence when dropdowns are changed
# TODO: Add axes labels, titles
# TODO: add tip/tilt scatter with colours going backwards in time


st.set_page_config(layout="wide")

st.title('Motor control for Heimdallr')


if 'motor1' not in st.session_state:
    import pyvisa
    st.session_state['motor1'] = M100D('ASRL/dev/ttyUSB0::INSTR', pyvisa.ResourceManager())
    st.session_state['motor2'] = M100D('ASRL/dev/ttyUSB1::INSTR', pyvisa.ResourceManager())


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
    with st.echo(code_location='below'):
        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.scatter(
            np.array([pos[0]]),
            np.array([pos[1]]),
        )

        ax.set_xlabel("x")
        ax.set_ylabel("y")

        ax.set_xlim(st.session_state[motor_key].BOUNDS[M100D.AXES.U])
        ax.set_ylim(st.session_state[motor_key].BOUNDS[M100D.AXES.V])

        st.write(fig)



with col2:
    TipTiltMotor()
#    beam = st.selectbox("Pick a component", list(range(1,5)))



