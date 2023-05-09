import streamlit as st
from newport_motors.Motors.motor import M100D

class InstrumentGUI:
    def create_GUI():
        pass

    def get_update_fn(source) -> callable:
        # whenever a value of the desired state changes, this function will be used as the callback. 
        # the input `source` will give information as to the reason for the callback and this function 
        # shall create the correct callable
        # e.g. if a tip tilt motor button changes, the source would be 'tiptilt' and the function would call
        # the apropriate version of the hardware call to update both axes of the motor 
        if source == 'x':
            axis = M100D.AXES.U
        elif source == 'y':
            axis = M100D.AXES.V
        else:
            raise NotImplementedError()
        def fn():
            print(f"sending {st.session_state[source]} to {st.session_state.component}")
            # print(st.session_state['motor'].read_pos(M100D.AXES.U))
            st.session_state['motor'].set_absolute_position(st.session_state[source], axis)
        return fn