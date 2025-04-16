from .base import BaseInstruction

class JumpInstruction(BaseInstruction):
    """Base class for jump instructions."""
    
    def should_jump(self):
        raise NotImplementedError("Subclasses must implement should_jump()")
    
    def execute(self, operands):
        if self.should_jump():
            return operands[0]  # Return label for jump
        return None


class JmpInstruction(JumpInstruction):
    """Handler for unconditional JMP instruction."""
    
    def should_jump(self):
        return True


class JzInstruction(JumpInstruction):
    """Handler for JZ (Jump if Zero) instruction."""
    
    def should_jump(self):
        return self.cpu.ZF


class JnzInstruction(JumpInstruction):
    """Handler for JNZ (Jump if Not Zero) instruction."""
    
    def should_jump(self):
        return not self.cpu.ZF


class JcInstruction(JumpInstruction):
    """Handler for JC (Jump if Carry) instruction."""
    
    def should_jump(self):
        return self.cpu.CF


class JncInstruction(JumpInstruction):
    """Handler for JNC (Jump if Not Carry) instruction."""
    
    def should_jump(self):
        return not self.cpu.CF


class LoopInstruction(BaseInstruction):
    """Handler for LOOP instruction."""
    
    def execute(self, operands):
        self.cpu.CX -= 1
        if self.cpu.CX != 0:
            return operands[0]  # Return label for jump
        return None 