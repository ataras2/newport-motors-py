import streamlit as st

class CustomNumeric:
    def variable_increment(key, callback_fn):
        if key not in st.session_state:
            st.session_state[key] = 0.


        inc = st.number_input('Step size', value=0.01, min_value=0., max_value=0.1, key='increment', step=0.005)
        x = st.number_input('x', value=st.session_state[key], min_value=-0.75, max_value=0.75, key=key, step = inc, on_change=callback_fn)

        # st.write('x Position = ', st.session_state['x'])