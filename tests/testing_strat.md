# Testing stratagy


## Overall approach
It would be nice to test the GUI and such without being connected to any motors. It would also be nice to test algorithms for controlling the motors without physically moving the motors. 
The pyvisa-mock library seems to be a good solution for this, where you can write a class to pretend to be a serial object that responds to certain commands.

Once these mock's are written, how can you be sure they are functionally correct in the way you care about them? We propose a few sets of tests:

1. User tests of the final GUI on the full version (acceptance tests)
2. Tests manually on the GUI elements of each motor (Integration tests)
3. testing low level functions through mocks (unit tests of the hardware interfacing code)
4. Testing the validity of the mocks (?? testing)

