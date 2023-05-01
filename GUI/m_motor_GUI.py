import streamlit as st
import pandas as pd
import numpy as np


st.title('Motor control for Heimdallr')

# error here, on change uses the previous value of component or beam 
# i.e. the call back occurs before beam assignment...
def on_item_change():
   print(f"Changing internals to {component}{beam}")


col1, col2 = st.columns(2)

with col1:
   component = st.selectbox("Pick a component", ["OAP1","Spherical mirror"], on_change=on_item_change)

with col2:
   beam = st.selectbox("Pick a component", list(range(1,5)), on_change=on_item_change)

st.write(f"Currently looking at {component}, beam {beam}")


