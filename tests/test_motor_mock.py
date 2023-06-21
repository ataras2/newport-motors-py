"""
Who tests the tester?
"""

from visa_mock.base.register import register_resource
from pyvisa import ResourceManager

from newport_motors.Mocks.motor import Mock_M100D, Mock_LS16P


register_resource("MOCK0::mock1::INSTR", Mock_M100D())
register_resource("MOCK0::mock2::INSTR", Mock_LS16P())

rc = ResourceManager(visa_library="@mock")
M100D_resource = rc.open_resource("MOCK0::mock1::INSTR")
LS16P_resource = rc.open_resource("MOCK0::mock2::INSTR")


class Test_Mock_M100D:
    def test_nothing(self):
        pass

    def test_id(self):
        id_str = M100D_resource.query("1ID?")
        assert "M100D" in id_str

    def test_get_abs_pos(self):
        # check that the return can be converted to a float
        reply = M100D_resource.query("1TPU")
        assert "1TPU" in reply

        float(reply[4:])


class Test_Mock_LS16P:
    def test_nothing(self):
        pass

    def test_id(self):
        id_str = LS16P_resource.query("1ID?")
        assert "LS16P" in id_str

    def test_get_abs_pos(self):
        # check that the return can be converted to a float
        reply = M100D_resource.query("1TP")
        assert "1TP" in reply
        float(reply[4:])
