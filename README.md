# newport_motors


## install
To use the sim env with pyvisa mock, you must manually change a line in the pyvisa file to correctly find the mock package. Change line 2820 in `highlevel.py` to use "pyvisa" instead of "pyvisa_". Then, when running in sim, create the resource manager like `pyvisa.ResourceManager(visa_library="@-mock")` and if for real use `pyvisa.ResourceManager(visa_library="@-py")`


