from .base import BaseInstruction

class CmpInstruction(BaseInstruction):
    """Handler for CMP instruction."""
    
    def execute(self, operands):
        dest, src = operands
        dest_value = self.parse_operand(dest)
        src_value = self.parse_operand(src)
        
        # Perform comparison and set flags
        result = dest_value - src_value
        
        # Set Zero Flag (ZF)
        self.cpu.ZF = 1 if result == 0 else 0
        
        # Set Sign Flag (SF)
        self.cpu.SF = 1 if (result & 0x8000) else 0
        
        # Set Carry Flag (CF)
        self.cpu.CF = 1 if src_value > dest_value else 0
        
        # Set Overflow Flag (OF)
        # Overflow occurs when subtracting numbers with different signs
        # and the result has the wrong sign
        dest_sign = dest_value & 0x8000
        src_sign = src_value & 0x8000
        result_sign = result & 0x8000
        
        self.cpu.OF = 1 if (dest_sign != src_sign) and (dest_sign != result_sign) else 0