class BaseInstruction:
    """Base class for all instruction handlers."""
    
    def __init__(self, cpu):
        self.cpu = cpu

    def execute(self, operands):
        """Execute the instruction with the given operands."""
        raise NotImplementedError("Subclasses must implement execute()")

    def parse_operand(self, operand):
        """Parse an operand into its value, handling registers, memory, and immediate values."""
        if operand.startswith('[') and operand.endswith(']'):
            # Memory reference
            address_expr = operand[1:-1]
            if '+' in address_expr:
                base, offset = address_expr.split('+')
                base = base.strip()
                offset = offset.strip()
                if base in ["BX", "BP", "SI", "DI"]:
                    base_value = self.cpu.get_register_value(base)
                    if offset.isdigit():
                        address = base_value + int(offset)
                    else:
                        address = base_value + self.cpu.get_register_value(offset)
                else:
                    raise ValueError(f"Invalid base register in memory reference: {base}")
            else:
                if address_expr in ["BX", "BP", "SI", "DI"]:
                    address = self.cpu.get_register_value(address_expr)
                else:
                    address = parse_hex_string(address_expr)
            return self.cpu.memory.read(address)
        elif operand in ["AX", "BX", "CX", "DX", "SI", "DI", "BP", "SP", "CS", "DS", "SS", "ES"]:
            return self.cpu.get_register_value(operand)
        elif operand.startswith('0x'):
            return int(operand, 16)
        elif operand.endswith('H'):
            return int(operand[:-1], 16)
        else:
            return int(operand) 