"""
Who tests the tester?
"""

from visa_mock.base.register import register_resource
from pyvisa import ResourceManager

from Mockers import Mock_M100D

class Test_Mock_M100D:
    def test_nothing(self):
        pass

    def _setup_mocks():
        register_resource("MOCK0::mock1::INSTR", Mock_M100D())

        rc = ResourceManager(visa_library="@mock")
        res = rc.open_resource("MOCK0::mock1::INSTR")
        return res

    def test_get_abs_pos(self):
        resource = Test_Mock_M100D._setup_mocks()
        
        # check that the return can be converted to a float
        reply = float(resource.query("1TPU"))
        