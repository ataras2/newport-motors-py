import streamlit as st

if 'x' not in st.session_state:
    # run this only the first time the app is opened
    st.session_state['x'] = 0


inc = st.number_input('Step size', value=0, min_value=0, key='increment', step=1)

x = st.number_input('x', value=st.session_state['x'], key='x', step = inc)

st.write('x Position = ', st.session_state['x'])

