"""
Testing the motor code directly (i.e. the python code)
"""

from newport_motors.Motors.motor import M100D
from visa_mock.base.register import register_resource
from pyvisa import ResourceManager

from Mockers import Mock_M100D

register_resource("MOCK0::mock1::INSTR", Mock_M100D())


class Test_Mock_M100D:
    def test_nothing(self):
        pass

    def test_ctor(self):
        M100D("MOCK0::mock1::INSTR", ResourceManager(visa_library="@mock"))




