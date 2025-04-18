# 🔧 8086 ISA Simulator

This lightweight Intel 8086 simulator is built with Flask (backend) and React + Vite (frontend). It supports:

- Instruction parsing (MOV, ADD, SUB, CMP, PUSH, POP, JMP, JNC, JC, etc.)
- Flag manipulation (ZF, CF, SF, OF)
- Memory and register monitoring
- Stack operations
- Manual memory addressing via [addr] / [BX] / [SI]

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend
cd frontend
npm install
npm run dev
```

## What it Emulates

- 16-bit general purpose registers (AX, BX, CX, DX)
- Segment & index registers (CS, DS, SS, SI, DI)
- Byte-addressable memory (manual 16-bit support)
- No AL, AH (only full 16-bit register support)

## Example Program

```asm
MOV AX, 0x1234
MOV BX, 0x2000
MOV CX, 0x0034
MOV DX, 0x0012
MOV [BX], CX
MOV [BX+1], DX
```
