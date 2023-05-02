import streamlit as st

if 'x' not in st.session_state:
    st.session_state['x'] = 0

print("before:", st.session_state)

inc = st.number_input('Step size', value=0, key='increment', step=1)

print("after:", st.session_state)

x = st.number_input('x', value=st.session_state['x'], key='x', step = inc)

st.write('x Position = ', st.session_state['x'])

