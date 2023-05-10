from collections import defaultdict
from pyvisa import ResourceManager
from visa_mock.base.base_mocker import BaseMocker, scpi
from visa_mock.base.register import register_resource


class Mocker(BaseMocker):
    """
    The main mocker class. 
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
    def idn(self, address : int, axis : str) -> str: 
        """
        'vendor', 'model', 'serial', 'firmware'
        """
        return axis



register_resource("MOCK0::mock1::INSTR", Mocker())

rc = ResourceManager(visa_library="@mock")
res = rc.open_resource("MOCK0::mock1::INSTR")
reply = res.query("*IDN?")  
print(reply)
reply = res.query("1TPU")  
print(reply)
# reply = res.query("*?IDN?")  
# print(reply)
