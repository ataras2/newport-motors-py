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
    
    @scpi("<address>ID?")
    def getID(self, address : int) -> str: 
        return "M100D"
    
    @scpi("<address>TP<axis>")
    def get_abs_pos(self, address : int, axis : str) -> str: 
        return 0.01
    
    @scpi("<address>PAU<value>")
    def set_abs_pos_u(self, address : int, value : float) -> str: 
        pass

    @scpi("<address>PAV<value>")
    def set_abs_pos_v(self, address : int, value : float) -> str: 
        pass


class Mock_LS16P(MotorMocker):
    """
    Command set taken from 
    https://www.newport.com/mam/celum/celum_assets/resources/Super_Agilis_-_User_s_Manual.pdf?3
    """

    def __init__(self, call_delay: float = 0.0):
        super().__init__(call_delay=call_delay)


    @scpi("<address>ID?")
    def getID(self, address : int) -> str: 
        return "LS16P"
    
    @scpi("<address>TP")
    def get_abs_pos(self, address : int, axis : str) -> str: 
        return 0.0
    
    @scpi("<address>PAU<value>")
    def set_abs_pos_u(self, address : int, value : float) -> str: 
        pass