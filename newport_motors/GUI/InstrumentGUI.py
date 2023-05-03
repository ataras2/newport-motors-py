import streamlit as st


class InstrumentGUI:
    def create_GUI():
        pass

    def get_update_fn(source) -> callable:
        # whenever a value of the desired state changes, this function will be used as the callback. 
        # the input `source` will give information as to the reason for the callback and this function 
        # shall create the correct callable
        # e.g. if a tip tilt motor button changes, the source would be 'tiptilt' and the function would call
        # the apropriate version of the hardware call to update both axes of the motor 
        a = 2
        def fn():
            print(f"sending {st.session_state.x} to {st.session_state.component} (a={a})")
        return fn