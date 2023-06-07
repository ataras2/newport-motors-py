import streamlit as st
import pandas as pd
import numpy as np

from newport_motors.Motors.motor import M100D, LS16P
from newport_motors.GUI.TipTiltUI import TipTiltUI
from newport_motors.GUI.LinearUI import LinearUI
from newport_motors.Motors.instrument import Instrument

import pyvisa


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

run_in_sim = False


st.set_page_config(layout="wide")

st.title("Motor control for Heimdallr alignment")


if "instrument" not in st.session_state:
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


if st.button("Reset all motors"):
    st.session_state["instrument"].zero_all()

col1, col2 = st.columns(2)

with col1:
    component = st.selectbox(
        # "Pick a component", ["OAP1", "Spherical", "Knife_edge"], key="component"
        "Pick a component",
        ["Spherical", "Knife_edge"],
        key="component",
    )

with col2:
    # beam = st.selectbox("Pick a component", list(range(1, 5)), key="beam")
    beam = st.selectbox("Pick a component", list(range(1, 3)), key="beam")


st.write(f"Currently looking at {component}, beam {beam}")

logging.info(
    f'Motor 1: {st.session_state["instrument"]["Spherical_1_TipTilt"]._is_reversed}'
)

logging.info(
    f'Motor 2: {st.session_state["instrument"]["Spherical_2_TipTilt"]._is_reversed}'
)

col1, col2 = st.columns(2)

# with col1:
#     LinearUI.main('motor3')


with col2:
    # motor_key = f"instrument.{component}_{beam}_TipTilt"
    motor = st.session_state["instrument"][f"{component}_{beam}_TipTilt"]
    TipTiltUI.main(motor)
