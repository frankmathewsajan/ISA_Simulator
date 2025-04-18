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
    Supports complex operands like registers, memory addresses, and immediate values.
    """
    instructions = []
    label_map = {}
    current_line = 0

    # Split the code into lines and process each line
    for line in code.splitlines():
        line = line.split(';')[0].strip()  # Remove comments
        if not line:
            continue

        # Handle label lines (e.g., loop:)
        if ':' in line:
            label_name = line.split(':')[0].strip()
            label_map[label_name] = len(instructions)
            line = line.split(':')[1].strip()
            if not line:  # If only label on line
                continue

        parts = line.split()
        if not parts:  # Skip empty lines after processing
            continue

        operation = parts[0].upper()  # Normalize operation to uppercase
        operands = []
        
        # Process operands, handling complex cases
        if len(parts) > 1:
            operand_str = ' '.join(parts[1:])
            # Split by comma but preserve memory references
            temp_operands = []
            current = ''
            in_brackets = False
            
            for char in operand_str:
                if char == '[':
                    in_brackets = True
                elif char == ']':
                    in_brackets = False
                elif char == ',' and not in_brackets:
                    temp_operands.append(current.strip())
                    current = ''
                    continue
                current += char
            if current:
                temp_operands.append(current.strip())
            
            operands = [op.strip() for op in temp_operands]

        instruction = {
            'operation': operation,
            'operands': operands,
            'raw': line,
            'line_number': current_line
        }
        instructions.append(instruction)
        current_line += 1

    return EXECUTOR(instructions, label_map)


def EXECUTOR(instructions, label_map):
    """
    Executes the list of parsed instructions with support for jumps and improved error handling.
    """
    ip = 0  # instruction pointer
    max_instructions = 100  # Prevent infinite loops
    instruction_count = 0

    while ip < len(instructions) and instruction_count < max_instructions:
        instruction = instructions[ip]
        operation = instruction['operation']
        operands = instruction['operands']

        print(f"[{instruction['line_number']}] Executing: {instruction['raw']}")

        try:
            # Execute the instruction and get potential jump target
            jump_target = cpu.execute_instruction(operation, operands, ip)

            # Handle jumps
            if jump_target is not None:
                if jump_target in label_map:
                    ip = label_map[jump_target]
                else:
                    raise ValueError(f"Jump target '{jump_target}' not found")
            else:
                ip += 1  # Move to next instruction

            instruction_count += 1

        except Exception as e:
            error_msg = f"Error executing instruction at line {instruction['line_number']}: {instruction['raw']}\nError: {str(e)}"
            print(error_msg)
            return {
                'error': error_msg,
                'cpu_state': {
                    'AX': cpu.AX,
                    'BX': cpu.BX,
                    'CX': cpu.CX,
                    'DX': cpu.DX,
                    'SI': cpu.SI,
                    'DI': cpu.DI,
                    'BP': cpu.BP,
                    'SP': cpu.SP,
                    'CS': cpu.CS,
                    'DS': cpu.DS,
                    'SS': cpu.SS,
                    'ES': cpu.ES,
                    'ZF': cpu.ZF,
                    'CF': cpu.CF,
                    'SF': cpu.SF,
                    'OF': cpu.OF
                },
                'memory': memory.get_memory_dict()
            }

    if instruction_count >= max_instructions:
        error_msg = "Maximum instruction count exceeded. Possible infinite loop detected."
        print(error_msg)
        return {
            'error': error_msg,
            'cpu_state': {
                'AX': cpu.AX,
                'BX': cpu.BX,
                'CX': cpu.CX,
                'DX': cpu.DX,
                'SI': cpu.SI,
                'DI': cpu.DI,
                'BP': cpu.BP,
                'SP': cpu.SP,
                'CS': cpu.CS,
                'DS': cpu.DS,
                'SS': cpu.SS,
                'ES': cpu.ES,
                'ZF': cpu.ZF,
                'CF': cpu.CF,
                'SF': cpu.SF,
                'OF': cpu.OF
            },
            'memory': memory.get_memory_dict()
        }

    # Return final state
    return {
        'cpu_state': {
            'AX': cpu.AX,
            'BX': cpu.BX,
            'CX': cpu.CX,
            'DX': cpu.DX,
            'SI': cpu.SI,
            'DI': cpu.DI,
            'BP': cpu.BP,
            'SP': cpu.SP,
            'CS': cpu.CS,
            'DS': cpu.DS,
            'SS': cpu.SS,
            'ES': cpu.ES,
            'ZF': cpu.ZF,
            'CF': cpu.CF,
            'SF': cpu.SF,
            'OF': cpu.OF
        },
        'memory': memory.get_memory_dict()
    }


def from_mem(address):
    """
    Get item from memory
    """
    return memory.read(address)
