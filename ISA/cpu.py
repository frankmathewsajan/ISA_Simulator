from memory import parse_hex_string

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

        # General-purpose registers (16-bit)
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

        self.IP = 0x0  # Instruction Pointer

    def calculate_physical_address(self, segment, offset):
        """Calculate the physical address from segment and offset."""
        return (segment << 4) + offset

    def execute_instruction(self, instruction, operands, instruction_index=None):
        """Execute an instruction (for example MOV, ADD, etc.)."""
        print(f"Executing: {instruction} {operands}")  # For debugging

        if instruction == "MOV":
            dest, src = operands
            # Convert src to integer if it's in hexadecimal format or decimal
            if src.startswith('0x'):
                src_value = int(src, 16)
            elif src.startswith('['):
                address_str = src[1:-1]
                if address_str in INDEX_REGS:
                    address_str = getattr(self, address_str)
                address = parse_hex_string(address_str)
                src_value = self.memory.read(address)
            elif src.endswith('H'):
                src_value = int(src[:-1], 16)  # Hexadecimal value
            elif src in GENERAL_REG:  # Check if src is a register
                src_value = getattr(self, src)  # Get the value of the register
            else:
                src_value = int(src)  # Treat as immediate value

            # Handle destination (dest) as either a register or memory
            if dest in GENERAL_REG:  # If destination is a register
                setattr(self, dest, src_value)  # Update register with src_value
            elif dest in INDEX_REGS:  # Index registers
                setattr(self, dest, src_value)
            elif dest.startswith("["):  # Memory operation
                # Strip brackets and parse 8086-style hex like 2000H
                address_str = dest[1:-1]
                if address_str in INDEX_REGS:
                    address_str = getattr(self, address_str)
                address = parse_hex_string(address_str)

                self.memory.write(address, src_value)

            else:
                raise ValueError(f"Unknown destination operand: {dest}")

        elif instruction == "ADD":
            dest, src = operands

            # Convert operands to integers (registers or immediate values)
            if src.startswith('0x'):
                src_value = int(src, 16)
            elif src in GENERAL_REG:  # Check if src is a register
                src_value = getattr(self, src)  # Get the value of the register
            else:
                src_value = int(src)  # Treat as immediate value

            if dest in GENERAL_REG:  # Register operand
                setattr(self, dest, getattr(self, dest) + src_value)
            elif dest.startswith("["):  # Memory operand
                address = int(dest[1:-1], 16)  # Memory address in hex
                current_value = self.memory.read(address)
                self.memory.write(address, current_value + src_value)
            else:
                raise ValueError(f"Unknown destination operand: {dest}")

        elif instruction == "PUSH":
            # For simplicity, we use the stack (SS) and the value in AX for push
            self.SS -= 2  # Stack grows downward
            address = self.calculate_physical_address(self.SS, 0)
            self.memory.write(address, self.AX)

        elif instruction == "POP":
            # Pop value from stack
            address = self.calculate_physical_address(self.SS, 0)
            self.AX = self.memory.read(address)
            self.SS += 2  # Stack shrinks upwards

        elif instruction in ("DEC", "INC"):
            k = 1 if instruction == "INC" else -1
            dest = operands[0]
            if isinstance(dest, str):  # Register
                setattr(self, dest, getattr(self, dest) + k)
            else:  # Memory Address (handling as tuple of segment and offset)
                segment, offset = dest
                address = self.calculate_physical_address(segment, offset)
                current_value = self.memory.read(address)
                self.memory.write(address, current_value + k)

        elif instruction == "JNZ":
            label = operands[0]
            # Check ZF to decide the jump
            if self.ZF != 0:
                # You would handle label jumps here (for simplicity, just printing label)
                print(f"Jumping to label: {label}")
            else:
                print("Not jumping, CX is zero.")
        elif instruction == "JMP":
            label = operands[0]
            # Handle unconditional jump
            print(f"Jumping to label: {label}")
        elif instruction == "label":
            print("Uff brother", operands[0])
        elif instruction == "CMP":
            dest, src = operands

            # Get dest value
            if dest in GENERAL_REG:
                dest_value = getattr(self, dest)
            elif dest.startswith("["):
                address = parse_hex_string(dest[1:-1])
                dest_value = self.memory.read(address)
            else:
                dest_value = int(dest)

            # Get src value
            if src in GENERAL_REG:
                src_value = getattr(self, src)
            elif src.startswith("["):
                address = parse_hex_string(src[1:-1])
                src_value = self.memory.read(address)
            elif src.startswith('0x'):
                src_value = int(src, 16)
            else:
                src_value = int(src)

            # Set Zero Flag based on the comparison
            self.ZF = int(dest_value == src_value)

        elif instruction == "LOOP":
            label = operands[0]
            # Decrement CX (loop counter)
            self.CX -= 1
            # If CX is not zero, jump to the label
            if self.CX != 0:
                print(f"Jumping to label: {label}")
            else:
                print("Loop completed, CX is zero.")

        else:
            raise ValueError(f"Unknown instruction: {instruction}")
