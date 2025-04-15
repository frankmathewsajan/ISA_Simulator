class Memory:
    def __init__(self):
        # Initialize 1MB memory space (1024 * 1024 bytes)
        self.memory = [0] * (1024 * 1024)

    def read(self, address):
        """Read from memory at a given physical address."""
        if 0 <= address < len(self.memory):
            return self.memory[address]
        else:
            raise ValueError("Memory address out of range.")

    def write(self, address, value):
        """Write to memory at a given physical address."""
        if 0 <= address < len(self.memory):

            self.memory[address] = value
        else:
            raise ValueError("Memory address out of range.")

    def get_memory_dict(self):
        """Return a dictionary representation of the memory."""
        return {hex(address): value for address, value in enumerate(self.memory) if value != 0}


def parse_hex_string(value):
    if isinstance(value, str) and value.endswith('H'):
        return int(value[:-1], 16)
    return int(value)
