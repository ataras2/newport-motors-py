import streamlit as st

if 'current_values' not in st.session_state:
    st.session_state['current_values'] = {
                                            'OAP1' : 0.01,
                                            'Spherical mirror' : 0.5,
                                            'Knife edge' : -0.3
                                        }


st.set_page_config(layout="wide")

st.title('Testing ways of making the values of numerics update correctly')

if 'x' not in st.session_state:
    st.session_state['x'] = 0.

def select_new_object():
    print(st.session_state['component'])
    st.session_state['x'] = st.session_state['current_values'][st.session_state['component']]
    

component = st.selectbox("Pick a component", 
                         ["OAP1","Spherical mirror","Knife edge"], 
                         key="component", 
                         on_change=select_new_object)


def update_cur_values():
    st.session_state['current_values'][st.session_state['component']] = st.session_state['x']
    print(st.session_state['current_values'])


st.number_input('x', 
                value=st.session_state['x'], 
                min_value=-0.75, 
                max_value=0.75, 
                key='x', 
                step = 0.01, 
                on_change=update_cur_values,
                format="%.3f")
