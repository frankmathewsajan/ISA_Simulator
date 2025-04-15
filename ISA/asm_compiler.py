"""
+-----------------------+
|    Assembly Parser    | ← converts raw string → instruction objects
+-----------------------+
|   Instruction Engine  |  ← decodes and dispatches execution logic
+-----------------------+
|   CPU Core (Executor) |  ← updates registers, memory, flags
+-----------------------+
|    Registers & Flags  |  ← state containers (AX, BX, ZF, CF, etc.)
+-----------------------+
|     Memory Module     |  ← raw addressable memory
+-----------------------+
|      Output Layer     |  ← returns final state to frontend
+-----------------------+
"""
from memory import Memory
from cpu import CPU

# Initialize memory and CPU
memory = Memory()
cpu = CPU(memory)


def COMPILE_ASM(code):
    """
    Compile the assembly code into a sequence of instructions.
    """
    return ASSEMBLY_PARSER(code)


def ASSEMBLY_PARSER(code):
    """
    Parse the assembly code and convert it into a list of instruction objects.
    """
    instructions = []
    label_map = {}

    # Split the code into lines and process each line
    for idx, line in enumerate(code.splitlines()):
        line = line.split(';')[0].strip()  # Remove comments
        if not line:
            continue

        parts = line.split()
        operation = parts[0]
        operands = [operand.strip(',') for operand in parts[1:]]

        # Handle label lines (e.g., loop:)
        if operation.endswith(':'):
            label_name = operation[:-1]
            label_map[label_name] = len(instructions)
            continue

        instruction = {
            'operation': operation,
            'operands': operands,
            'raw': line
        }
        instructions.append(instruction)

    return EXECUTOR(instructions, label_map)


def EXECUTOR(instructions, label_map):
    """
    Executes the list of parsed instructions with support for jumps.
    """
    ip = 0  # instruction pointer

    while ip < len(instructions):
        instruction = instructions[ip]
        operation = instruction['operation']
        operands = instruction['operands']

        print(f"[{ip}] Executing: {instruction['raw']}")

        if operation == "JMP":
            label = operands[0]
            if label in label_map:
                ip = label_map[label]
                continue
            else:
                print(f"Error: Label '{label}' not found.")
                break

        elif operation == "JNZ":
            if cpu.ZF == 0:
                label = operands[0]
                if label in label_map:
                    ip = label_map[label]
                    continue
                else:
                    print(f"Error: Label '{label}' not found.")
                    break
            else:
                ip += 1
                continue

        else:
            try:
                cpu.execute_instruction(operation, operands)
            except Exception as e:
                print(f"Error executing instruction {instruction['raw']}: {e}")
            ip += 1  # Move to next instruction

    # Output final CPU state
    print(f"\nFinal CPU State:")
    print(f"AX: {cpu.AX}, BX: {cpu.BX}, CX: {cpu.CX}, DX: {cpu.DX}, ZF: {cpu.ZF}")
    print(memory.get_memory_dict())

    return instructions


def from_mem(address):
    """
    Get item from memory
    """
    return memory.read(address)
