import streamlit as st
import pandas as pd
import numpy as np

from newport_motors.Motors.motor import M100D, LS16P
from newport_motors.GUI.TipTiltUI import TipTiltUI
from newport_motors.GUI.LinearUI import LinearUI
from newport_motors.Motors.instrument import Instrument

import pyvisa

# TODO: have persistence when dropdowns are changed
# TODO: Add axes labels, titles
# TODO: add tip/tilt scatter with colours going backwards in time

import logging

from datetime import datetime
import os

now = datetime.now()  # current date and time
fname = now.strftime("%m_%d_%Y_%H_%M_%S")

logging.basicConfig(
    # filename=os.path.join('logs/', fname+".log"),
    encoding="utf-8",
    level=logging.INFO,
    format="%(filename)s:%(levelname)s: %(message)s",
)

run_in_sim = True


st.set_page_config(layout="wide")

st.title("Motor control for Heimdallr alignment")

# instrument_motor_config = [
#     {

#     }
# ]


def create_motor_sim():
    pass


def open_motor_connections():
    pass


if "motor1" not in st.session_state:
    if run_in_sim:
        from newport_motors.Mocks.motor import Mock_M100D, Mock_LS16P
        from visa_mock.base.register import register_resource

        motor1_port = "MOCK0::mock1::INSTR"
        motor2_port = "MOCK0::mock2::INSTR"
        motor3_port = "MOCK0::mock3::INSTR"

        register_resource(motor1_port, Mock_M100D())
        register_resource(motor2_port, Mock_M100D())
        register_resource(motor3_port, Mock_LS16P())

        resource_manager = pyvisa.ResourceManager(visa_library="@-mock")

        raise NotImplementedError()
    else:
        i = Instrument("InstrumentConfigs/Heimdallr_tt_only.json")
        resource_manager = pyvisa.ResourceManager(visa_library="@_py")

    st.session_state["instrument"] = i
    # st.session_state["motor1"] = M100D(motor1_port, resource_manager)
    # st.session_state["motor2"] = M100D(motor2_port, resource_manager)
    # st.session_state["motor1"].set_to_zero()
    # st.session_state["motor2"].set_to_zero()
    # st.session_state['motor3'] = LS16P(motor3_port, resource_manager)


col1, col2 = st.columns(2)

with col1:
    component = st.selectbox(
        "Pick a component", ["OAP1", "Spherical", "Knife_edge"], key="component"
    )

with col2:
    beam = st.selectbox("Pick a component", list(range(1, 5)), key="beam")


st.write(f"Currently looking at {component}, beam {beam}")


col1, col2 = st.columns(2)

# with col1:
#     LinearUI.main('motor3')


with col2:
    motor_key = f"instrument.{component}_{beam}_TipTilt"
    TipTiltUI.main(motor_key)
