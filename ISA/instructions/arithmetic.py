from .base import BaseInstruction

class AddInstruction(BaseInstruction):
    """Handler for ADD instruction."""
    
    def execute(self, operands):
        dest, src = operands
        src_value = self.parse_operand(src)
        dest_value = self.parse_operand(dest)
        
        result = dest_value + src_value
        self.cpu.CF = int(result > 0xFFFF)
        self.cpu.ZF = int(result == 0)
        self.cpu.SF = int(result & 0x8000 != 0)
        self.cpu.OF = int((dest_value ^ src_value) & 0x8000 == 0 and (dest_value ^ result) & 0x8000 != 0)
        
        if dest.startswith('['):
            # Memory destination
            address = self.parse_operand(dest)
            self.cpu.memory.write(address, result & 0xFFFF)
        else:
            # Register destination
            self.cpu.set_register_value(dest, result & 0xFFFF)


class SubInstruction(BaseInstruction):
    """Handler for SUB instruction."""
    
    def execute(self, operands):
        dest, src = operands
        src_value = self.parse_operand(src)
        dest_value = self.parse_operand(dest)
        
        result = dest_value - src_value
        self.cpu.CF = int(result < 0)
        self.cpu.ZF = int(result == 0)
        self.cpu.SF = int(result & 0x8000 != 0)
        self.cpu.OF = int((dest_value ^ src_value) & 0x8000 != 0 and (dest_value ^ result) & 0x8000 != 0)
        
        if dest.startswith('['):
            # Memory destination
            address = self.parse_operand(dest)
            self.cpu.memory.write(address, result & 0xFFFF)
        else:
            # Register destination
            self.cpu.set_register_value(dest, result & 0xFFFF)


class IncInstruction(BaseInstruction):
    """Handler for INC instruction."""
    
    def execute(self, operands):
        dest = operands[0]
        dest_value = self.parse_operand(dest)
        
        result = dest_value + 1
        self.cpu.ZF = int(result == 0)
        self.cpu.SF = int(result & 0x8000 != 0)
        self.cpu.OF = int(result == 0x8000)  # Overflow if result is -32768
        
        if dest.startswith('['):
            # Memory destination
            address = self.parse_operand(dest)
            self.cpu.memory.write(address, result & 0xFFFF)
        else:
            # Register destination
            self.cpu.set_register_value(dest, result & 0xFFFF)


class DecInstruction(BaseInstruction):
    """Handler for DEC instruction."""
    
    def execute(self, operands):
        dest = operands[0]
        dest_value = self.parse_operand(dest)
        
        result = dest_value - 1
        self.cpu.ZF = int(result == 0)
        self.cpu.SF = int(result & 0x8000 != 0)
        self.cpu.OF = int(result == 0x7FFF)  # Overflow if result is 32767
        
        if dest.startswith('['):
            # Memory destination
            address = self.parse_operand(dest)
            self.cpu.memory.write(address, result & 0xFFFF)
        else:
            # Register destination
            self.cpu.set_register_value(dest, result & 0xFFFF) 