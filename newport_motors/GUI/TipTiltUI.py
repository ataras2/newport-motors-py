import streamlit as st
import numpy as np

import logging

from newport_motors.GUI.CustomNumeric import CustomNumeric
from newport_motors.GUI.InstrumentGUI import InstrumentGUI

from newport_motors.Motors.motor import M100D


class TipTiltUI:
    def main(motor_key : str):
        st.header("Tip/Tilt motor")
        CustomNumeric.variable_increment(['tip_tilt_u', 'tip_tilt_v'],
                                        [TipTiltUI.get_callback('tip_tilt_u', motor_key), 
                                         TipTiltUI.get_callback('tip_tilt_v', motor_key)],
                                        st.session_state[motor_key].get_current_pos(),
                                        main_bounds=M100D.HW_BOUNDS[M100D.AXES.V])
        pos = st.session_state[motor_key].get_current_pos()
        logging.info(pos)

        import plotly.express as px

        fig = px.scatter(
            x=np.array([pos[1]]),
            y=np.array([pos[0]]),
        )
        fig.update_layout(
            xaxis_title="x",
            yaxis_title="y",
            yaxis = dict(range=st.session_state[motor_key].HW_BOUNDS[M100D.AXES.V][::-1]),
            xaxis = dict(range=st.session_state[motor_key].HW_BOUNDS[M100D.AXES.U][::-1])
        )

        st.write(fig)

    def get_callback(source : str, motor_key : str) -> callable:
        if source[-1] == 'u':
            axis = M100D.AXES.U
        elif source[-1] == 'v':
            axis = M100D.AXES.V
        else:
            raise NotImplementedError()
        def fn():
            logging.info(f"sending {st.session_state[source]} to {st.session_state.component}")
            st.session_state[motor_key].set_absolute_position(st.session_state[source], axis)
        return fn