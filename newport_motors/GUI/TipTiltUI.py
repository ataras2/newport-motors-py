import streamlit as st
import numpy as np

import logging

from newport_motors.GUI.CustomNumeric import CustomNumeric
from newport_motors.GUI.InstrumentGUI import InstrumentGUI

from newport_motors.Motors.motor import M100D


class TipTiltUI:
    @staticmethod
    def main(motor_key: str):
        """
        Create a UI block to control a tip/tilt motor, featuring a numeric input for the increment,
        a numeric input for the absolute position of each axis, and a scatter plot of the current position

        Parameters:
            motor_key (str) : the key to use to store the motor in the session state
        """
        st.header("Tip/Tilt motor")
        CustomNumeric.variable_increment(
            ["tip_tilt_u", "tip_tilt_v"],
            [
                TipTiltUI.get_callback("tip_tilt_u", motor_key, M100D.AXES.U),
                TipTiltUI.get_callback("tip_tilt_v", motor_key, M100D.AXES.V),
            ],
            st.session_state[motor_key].get_current_pos,
            main_bounds=M100D.HW_BOUNDS[M100D.AXES.V],
        )
        pos = st.session_state[motor_key].get_current_pos
        logging.info(pos)

        import plotly.express as px

        fig = px.scatter(
            x=np.array([pos[0]]),
            y=np.array([pos[1]]),
        )
        fig.update_layout(
            xaxis_title="v",
            yaxis_title="u",
            xaxis=dict(range=st.session_state[motor_key].HW_BOUNDS[M100D.AXES.U][::]),
            yaxis=dict(range=st.session_state[motor_key].HW_BOUNDS[M100D.AXES.V][::]),
        )

        st.write(fig)

    @staticmethod
    def get_callback(source: str, motor_key: str, axis: M100D.AXES) -> callable:
        """
        Return a callback function to set the absolute position of the motor in a given axis

        Parameters:
            source (str) : the key to use to store the value to move to in the session state
            motor_key (str) : the key to use to store the motor in the session state
            axis (M100D.AXES) : the axis to set
        """

        def fn():
            logging.info(
                f"sending {st.session_state[source]} to {st.session_state.component}"
            )
            st.session_state[motor_key].set_absolute_position(
                st.session_state[source], axis
            )

        return fn
