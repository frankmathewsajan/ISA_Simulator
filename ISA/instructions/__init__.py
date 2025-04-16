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
    'mov': MovInstruction,
    'add': AddInstruction,
    'sub': SubInstruction,
    'inc': IncInstruction,
    'dec': DecInstruction,
    'push': PushInstruction,
    'pop': PopInstruction,
    'jmp': JmpInstruction,
    'jz': JzInstruction,
    'jnz': JnzInstruction,
    'cmp': CmpInstruction,
    'JC': JcInstruction,
    'JNC': JncInstruction,
    'LOOP': LoopInstruction,
} 