from .base import BaseInstruction
from .mov import MovInstruction
from .arithmetic import AddInstruction, SubInstruction, IncInstruction, DecInstruction
from .stack import PushInstruction, PopInstruction
from .jump import (
    JmpInstruction, JzInstruction, JnzInstruction,
    JcInstruction, JncInstruction, LoopInstruction
)
from .compare import CmpInstruction

# Map instruction names to their handlers
INSTRUCTION_HANDLERS = {
    'MOV': MovInstruction,
    'ADD': AddInstruction,
    'SUB': SubInstruction,
    'INC': IncInstruction,
    'DEC': DecInstruction,
    
    # Stack Operations 
    'PUSH': PushInstruction,
    'POP': PopInstruction,
    
    # Unconditional Jumps
    'JMP': JmpInstruction,
    
    # Conditional Jumps @ ZF =1
    'JZ': JzInstruction,
    'JE': JzInstruction,
    
    # Conditional Jumps @ ZF = 0
    'JNZ': JnzInstruction,
    'JNE': JnzInstruction,
    
    'CMP': CmpInstruction,
    # Carry Flag Jumps
    'JC': JcInstruction,
    'JNC': JncInstruction,
    # Loop
    'LOOP': LoopInstruction,
}