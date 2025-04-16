from .base import BaseInstruction

class PushInstruction(BaseInstruction):
    """Handler for PUSH instruction."""
    
    def execute(self, operands):
        reg = operands[0]
        value = self.cpu.get_register_value(reg)
        self.cpu.SP -= 2
        address = self.cpu.calculate_physical_address(self.cpu.SS, self.cpu.SP)
        self.cpu.memory.write(address, value)


class PopInstruction(BaseInstruction):
    """Handler for POP instruction."""
    
    def execute(self, operands):
        reg = operands[0]
        address = self.cpu.calculate_physical_address(self.cpu.SS, self.cpu.SP)
        value = self.cpu.memory.read(address)
        self.cpu.set_register_value(reg, value)
        self.cpu.SP += 2 