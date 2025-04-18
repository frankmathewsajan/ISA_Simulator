from memory import parse_hex_string
from instructions import INSTRUCTION_HANDLERS

GENERAL_REG = ["AX", "BX", "CX", "DX"]
INDEX_REGS = ["SI", "DI", "BP", "SP"]


class CPU:
    def __init__(self, memory):
        self.memory = memory

        # 16-bit segment registers (each can hold 16-bit values)
        self.CS = 0x0  # Code Segment
        self.DS = 0x0  # Data Segment
        self.SS = 0x0  # Stack Segment
        self.ES = 0x0  # Extra Segment

        # 16-bit general-purpose registers
        self.AX = 0x0
        self.BX = 0x0
        self.CX = 0x0
        self.DX = 0x0


        # Index registers (16-bit)
        self.SI = 0x0  # Source Index
        self.DI = 0x0  # Destination Index
        self.BP = 0x0  # Base Pointer
        self.SP = 0x0  # Stack Pointer

        # Flags register (16-bit)
        self.ZF = 0  # Zero Flag
        self.CF = 0  # Carry Flag
        self.SF = 0  # Sign Flag
        self.OF = 0  # Overflow Flag

        self.IP = 0x0  # Instruction Pointer

        # Initialize instruction handlers
        self.instruction_handlers = {
            name: handler(self) for name, handler in INSTRUCTION_HANDLERS.items()
        }

    def calculate_physical_address(self, segment, offset):
        """Calculate the physical address from segment and offset."""
        return (segment << 4) + offset

    def get_register_value(self, reg):
        """Get the value of a register by name."""
        if reg in ["AX", "BX", "CX", "DX", "SI", "DI", "BP", "SP"]:
            return getattr(self, reg)
        elif reg in ["CS", "DS", "SS", "ES"]:
            return getattr(self, reg)
        elif reg in ["AH", "AL", "BH", "BL", "CH", "CL", "DH", "DL"]:
            return getattr(self, reg)
        raise ValueError(f"Unknown register: {reg}")

    def set_register_value(self, reg, value):
        """Set the value of a register by name."""
        if reg in ["AX", "BX", "CX", "DX", "SI", "DI", "BP", "SP"]:
            setattr(self, reg, value & 0xFFFF)  # Ensure 16-bit value
            # Update 8-bit parts for AX, BX, CX, DX
            if reg == "AX":
                self.AH = (value >> 8) & 0xFF
                self.AL = value & 0xFF
            elif reg == "BX":
                self.BH = (value >> 8) & 0xFF
                self.BL = value & 0xFF
            elif reg == "CX":
                self.CH = (value >> 8) & 0xFF
                self.CL = value & 0xFF
            elif reg == "DX":
                self.DH = (value >> 8) & 0xFF
                self.DL = value & 0xFF
        elif reg in ["CS", "DS", "SS", "ES"]:
            setattr(self, reg, value & 0xFFFF)
    
        else:
            raise ValueError(f"Unknown register: {reg}")

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
                    base_value = self.get_register_value(base)
                    if offset.isdigit():
                        address = base_value + int(offset)
                    else:
                        address = base_value + self.get_register_value(offset)
                else:
                    raise ValueError(f"Invalid base register in memory reference: {base}")
            else:
                if address_expr in ["BX", "BP", "SI", "DI"]:
                    address = self.get_register_value(address_expr)
                else:
                    address = parse_hex_string(address_expr)
            return self.memory.read(address)
        elif operand in ["AX", "BX", "CX", "DX", "SI", "DI", "BP", "SP", "CS", "DS", "SS", "ES"]:
            return self.get_register_value(operand)
        elif operand.startswith('0x'):
            return int(operand, 16)
        elif operand.endswith('H'):
            return int(operand[:-1], 16)
        else:
            return int(operand)

    def execute_instruction(self, instruction, operands, instruction_index=None):
        """Execute an instruction using the appropriate handler."""
        instruction = instruction.upper()
        if instruction not in self.instruction_handlers:
            raise ValueError(f"Unknown instruction: {instruction}")
        
        handler = self.instruction_handlers[instruction]
        return handler.execute(operands)
