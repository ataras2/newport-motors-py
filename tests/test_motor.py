"""
Testing the motor code directly (i.e. the python code)
"""

from newport_motors.Motors.motor import M100D, LS16P
from visa_mock.base.register import register_resource
from pyvisa import ResourceManager

from newport_motors.Mocks.motor import Mock_M100D, Mock_LS16P

register_resource("MOCK0::mock1::INSTR", Mock_M100D())
register_resource("MOCK0::mock2::INSTR", Mock_LS16P())


class Test_M100D:
    def test_nothing(self):
        pass

    def test_ctor(self):
        M100D("MOCK0::mock1::INSTR", ResourceManager(visa_library="@-mock"))

    def test_move(self):
        m = M100D("MOCK0::mock1::INSTR", ResourceManager(visa_library="@-mock"))
        m.set_absolute_position(0.2, M100D.AXES.U)

        assert m.get_current_pos()[0] == 0.2

    def test_read(self):
        m = M100D("MOCK0::mock1::INSTR", ResourceManager(visa_library="@-mock"))
        p = m.read_pos(M100D.AXES.U)

        assert isinstance(p, float)
        assert p > -0.75 and p < 0.75



class Test_LS16P:
    def test_nothing(self):
        pass

    def test_ctor(self):
        LS16P("MOCK0::mock2::INSTR", ResourceManager(visa_library="@-mock"))


