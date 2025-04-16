# 8086-like Assembly Language Emulator

This is a Python-based emulator for a simplified 8086-like assembly language. It simulates a CPU executing assembly instructions, managing registers, flags, and memory operations.

## Input Format

The emulator accepts assembly code as a string input. The code should follow these conventions:

### Basic Syntax
- One instruction per line
- Comments start with `;`
- Labels end with `:`
- Operands are separated by commas
- Memory references use square brackets `[]`

### Supported Instructions

#### Data Movement
- `MOV dest, src` - Move data between registers/memory
  - Example: `MOV AX, 5` or `MOV [BX], AX`

#### Arithmetic
- `ADD dest, src` - Add values
  - Example: `ADD AX, BX`
- `SUB dest, src` - Subtract values
  - Example: `SUB AX, 5`

#### Stack Operations
- `PUSH reg` - Push register onto stack
  - Example: `PUSH AX`
- `POP reg` - Pop value from stack to register
  - Example: `POP BX`

#### Control Flow
- `JMP label` - Unconditional jump
  - Example: `JMP loop`
- `JZ label` - Jump if zero
  - Example: `JZ done`
- `JNZ label` - Jump if not zero
  - Example: `JNZ loop`
- `JC label` - Jump if carry
  - Example: `JC error`
- `JNC label` - Jump if not carry
  - Example: `JNC continue`
- `LOOP label` - Decrement CX and jump if not zero
  - Example: `LOOP repeat`

#### Comparison
- `CMP dest, src` - Compare values and set flags
  - Example: `CMP AX, BX`

### Operand Types

1. Registers:
   - General purpose: `AX`, `BX`, `CX`, `DX`
   - Index registers: `SI`, `DI`, `BP`, `SP`
   - Segment registers: `CS`, `DS`, `SS`, `ES`

2. Memory References:
   - Direct: `[0x1234]`
   - Register indirect: `[BX]`
   - Register + offset: `[BX+5]`

3. Immediate Values:
   - Decimal: `5`
   - Hexadecimal (H suffix): `5H`
   - Hexadecimal (0x prefix): `0x5`

### Example Program

```assembly
MOV AX, 5
MOV BX, 10
ADD AX, BX
CMP AX, 15
JZ done
MOV CX, 0
done: NOP
```

## Output Format

The emulator returns a JSON response with the following structure:

```json
{
    "error": null,
    "cpu_state": {
        "AX": 15,
        "BX": 10,
        "CX": 0,
        "DX": 0,
        "SI": 0,
        "DI": 0,
        "BP": 0,
        "SP": 0,
        "CS": 0,
        "DS": 0,
        "SS": 0,
        "ES": 0,
        "ZF": 1,
        "CF": 0,
        "SF": 0,
        "OF": 0
    },
    "memory": {
        "0x0": 5,
        "0x1": 10
    }
}
```

### Error Response

If an error occurs during execution, the response will include an error message:

```json
{
    "error": "Error executing instruction at line 3: MOV AX, invalid\nError: Invalid operand",
    "cpu_state": {
        // Current CPU state at time of error
    },
    "memory": {
        // Current memory state at time of error
    }
}
```

## API Usage

The emulator is accessible via a REST API endpoint:

```
POST /
Content-Type: application/json

{
    "code": "MOV AX, 5\nMOV BX, 10\nADD AX, BX"
}
```

Response:
```json
{
    "error": null,
    "cpu_state": {
        // CPU state after execution
    },
    "memory": {
        // Memory state after execution
    }
}
``` 