from .base import BaseInstruction

class MovInstruction(BaseInstruction):
    """Handler for MOV instruction."""
    
    def execute(self, operands):
        dest, src = operands
        src_value = self.parse_operand(src)

        if dest.startswith('[') and dest.endswith(']'):
            # Memory destination
            address_expr = dest[1:-1]
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
            self.cpu.memory.write(address, src_value)
        else:
            # Register destination
            self.cpu.set_register_value(dest, src_value) 