import streamlit as st
import numpy as np

import logging

from newport_motors.GUI.CustomNumeric import CustomNumeric
from newport_motors.GUI.InstrumentGUI import InstrumentGUI

from newport_motors.Motors.motor import LS16P


class LinearUI:
    def main(motor_key: str):
        st.header("Linear motor")
        CustomNumeric.variable_increment(
            ["displacement"],
            [LinearUI.get_callback("displacement", motor_key)],
            [st.session_state[motor_key].get_current_pos],
            main_bounds=LS16P.HW_BOUNDS,
        )

        pos = st.session_state[motor_key].get_current_pos
        logging.info(f"Current linear position: {pos}")

    def get_callback(source: str, motor_key: str) -> callable:
        def fn():
            logging.info(
                f"sending {st.session_state[source]} to {st.session_state.component}"
            )
            st.session_state[motor_key].set_absolute_position(st.session_state[source])

        return fn
