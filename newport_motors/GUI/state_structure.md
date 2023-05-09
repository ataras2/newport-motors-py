# Session state

## Purpose
This document outlines thoughts about the session state variable in a GUI application using this library

## Intro
The `st.session_state` dictionary in streamlit provides a way of maintaining state while the application reruns as new inputs come in. To have this work effectively in an application with mnay parts, a structure must be chosen.

## Discussion
There are two obvious candidates here:
 - a flat structure, where every key is unique and is accessed directly
 - a heirarchy, such that the top level keys only need to be unique but lower levels need to know how to access parts of it

The difficulty here is getting the abstraction right - each part of the app should control some piece of hardware and interact strongly with the hardware code. One step in the right direction is to put as much *relevant* information in the hardware class itself. For example, the motor class should store the current last position of the motor, and the GUI should access this when populating fields.

How should the GUI know what commands to send to the motor? The callback function needs to know the path to the data in the session state variable.


## Conclusion
Discussion still ongoing