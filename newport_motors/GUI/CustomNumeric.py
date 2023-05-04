import streamlit as st

class CustomNumeric:
    def variable_increment(keys : list[str], callback_fns : list[callable]):
        for key in keys:
            if key not in st.session_state:
                st.session_state[key] = 0.


        inc = st.number_input('Step size', 
                              value=0.01, 
                              min_value=0., 
                              max_value=0.1, 
                              key='increment', 
                              step=0.005,
                              format="%.3f")
        for c_fn, key in zip(callback_fns, keys):
            st.number_input(key, 
                            value=st.session_state[key], 
                            min_value=-0.75, 
                            max_value=0.75, 
                            key=key, 
                            step = inc, 
                            on_change=c_fn,
                            format="%.3f")

        # st.write('x Position = ', st.session_state['x'])