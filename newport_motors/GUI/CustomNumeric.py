import streamlit as st

class CustomNumeric:
    def variable_increment(callback_fn):
        if 'x' not in st.session_state:
            st.session_state['x'] = 0


        inc = st.number_input('Step size', value=0, min_value=0, key='increment', step=1)
        x = st.number_input('x', value=st.session_state['x'], key='x', step = inc, on_change=callback_fn)

        # st.write('x Position = ', st.session_state['x'])