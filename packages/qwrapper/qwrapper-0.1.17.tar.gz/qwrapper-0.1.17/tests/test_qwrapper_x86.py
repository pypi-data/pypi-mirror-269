from qwrapper import X86Machine
import time
from pygdbmi import gdbcontroller

# Create a machine
def test_x86machine_start():
    machine = X86Machine()




# Create machine and read memory
def test_x86_machine_memory():
    machine = X86Machine()
    
    memory_test = ['0x00', '0x00', '0x00']

    memory = machine.read_memory_bytes(0x0, 3)

    assert memory is not None

    assert memory == memory_test
