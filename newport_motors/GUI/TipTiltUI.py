import streamlit as st
import numpy as np

import logging

from newport_motors.GUI.CustomNumeric import CustomNumeric
from newport_motors.GUI.InstrumentGUI import InstrumentGUI

from newport_motors.Motors.motor import M100D, Motor


class TipTiltUI:
    @staticmethod
    def main(motor: Motor):
        """
        Create a UI block to control a tip/tilt motor, featuring a numeric input for the increment,
        a numeric input for the absolute position of each axis, and a scatter plot of the current position

        Parameters:
            motor_key (str) : the key to use to store the motor in the session state
        """
        st.header("Tip/Tilt motor")
        CustomNumeric.variable_increment(
            ["U", "V"],
            [
                TipTiltUI.get_callback("U", motor, M100D.AXES.U),
                TipTiltUI.get_callback("V", motor, M100D.AXES.V),
            ],
            motor.get_current_pos,
            main_bounds=M100D.HW_BOUNDS[M100D.AXES.V],
        )
        pos = motor.get_current_pos
        logging.info(pos)

        import plotly.express as px

        fig = px.scatter(
            x=np.array([pos[1]]),
            y=np.array([pos[0]]),
        )
        fig.update_layout(
            xaxis_title="v [deg]",
            yaxis_title="u [deg]",
            title="Current position reflection of on axis source",
            xaxis=dict(range=motor.HW_BOUNDS[M100D.AXES.V][::-1]),
            yaxis=dict(range=motor.HW_BOUNDS[M100D.AXES.U][::-1]),
        )

        st.write(fig)

    @staticmethod
    def get_callback(source: str, motor: Motor, axis: M100D.AXES) -> callable:
        """
        Return a callback function to set the absolute position of the motor in a given axis

        Parameters:
            source (str) : the key to use to store the value to move to in the session state
            motor (Motor) : the motor to control
            axis (M100D.AXES) : the axis to set
        """

        def fn():
            logging.info(
                f"sending {st.session_state[source]} to {st.session_state.component}, axis {axis}"
            )
            motor.set_absolute_position(st.session_state[source], axis)

        return fn
