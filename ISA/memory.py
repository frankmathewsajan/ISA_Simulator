class Memory:
    def __init__(self):
        # Initialize 1MB memory space (1024 * 1024 bytes)
        self.memory = bytearray(1024 * 1024)

    def read(self, address):
        """Read from memory at a given physical address."""
        if isinstance(address, tuple):
            segment, offset = address
            physical_address = (segment << 4) + offset
        else:
            physical_address = address

        if 0 <= physical_address < len(self.memory):
            return self.memory[physical_address]
        else:
            raise ValueError(f"Memory address out of range: {hex(physical_address)}")

    def write(self, address, value):
        """Write to memory at a given physical address."""
        if isinstance(address, tuple):
            segment, offset = address
            physical_address = (segment << 4) + offset
        else:
            physical_address = address

        if 0 <= physical_address < len(self.memory):
            self.memory[physical_address] = value & 0xFFFF  # Ensure 16-bit value
        else:
            raise ValueError(f"Memory address out of range: {hex(physical_address)}")

    def get_memory_dict(self):
        """Return a dictionary representation of the memory."""
        return {hex(address): value for address, value in enumerate(self.memory) if value != 0}

    def get_segment_address(self, segment_name):
        """Get the base address of a segment."""
        if segment_name in self.segments:
            return self.segments[segment_name]
        raise ValueError(f"Unknown segment: {segment_name}")

    def set_segment_address(self, segment_name, address):
        """Set the base address of a segment."""
        if segment_name in self.segments:
            self.segments[segment_name] = address & 0xFFFF  # Ensure 16-bit value
        else:
            raise ValueError(f"Unknown segment: {segment_name}")

    def read_word(self, address):
        """Read a 16-bit word from memory."""
        if isinstance(address, tuple):
            segment, offset = address
            physical_address = (segment << 4) + offset
        else:
            physical_address = address

        if physical_address + 1 >= len(self.memory):
            raise ValueError(f"Memory address out of range: {hex(physical_address)}")

        low_byte = self.memory[physical_address]
        high_byte = self.memory[physical_address + 1]
        return (high_byte << 8) | low_byte

    def write_word(self, address, value):
        """Write a 16-bit word to memory."""
        if isinstance(address, tuple):
            segment, offset = address
            physical_address = (segment << 4) + offset
        else:
            physical_address = address

        if physical_address + 1 >= len(self.memory):
            raise ValueError(f"Memory address out of range: {hex(physical_address)}")

        value = value & 0xFFFF  # Ensure 16-bit value
        self.memory[physical_address] = value & 0xFF  # Low byte
        self.memory[physical_address + 1] = (value >> 8) & 0xFF  # High byte


def parse_hex_string(value):
    """Parse a hexadecimal string into an integer."""
    if isinstance(value, str):
        if value.endswith('H'):
            return int(value[:-1], 16)
        elif value.startswith('0x'):
            return int(value, 16)
        elif value.isdigit():
            return int(value)
        else:
            raise ValueError(f"Invalid number format: {value}")
    return int(value)
