from visa_mock.base.base_mocker import BaseMocker, scpi

class MotorMocker(BaseMocker):
    """
    The main mocker class. 
    """

    def __init__(self, call_delay: float = 0.0):
        super().__init__(call_delay=call_delay)



class Mock_M100D(MotorMocker):
    """
    The mocker for the tip/tilt motor
    """

    def __init__(self, call_delay: float = 0.0):
        super().__init__(call_delay=call_delay)

    @scpi("*IDN?")
    def idn(self) -> str: 
        """
        'vendor', 'model', 'serial', 'firmware'
        """
        return "Mocker,testing,00000,0.01"
    
    @scpi("<address>TP<axis>")
    def get_abs_pos(self, address : int, axis : str) -> str: 
        return 0.01
    
    @scpi("<address>PAU<value>")
    def set_abs_pos_u(self, address : int, value : float) -> str: 
        pass

    @scpi("<address>PAV<value>")
    def set_abs_pos_v(self, address : int, value : float) -> str: 
        pass