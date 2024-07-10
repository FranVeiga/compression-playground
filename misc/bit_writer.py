class BitWriter:
    def __init__(self):
        self.out = b""
        self.buffer = 0
        self.buffer_size = 0

    def write_bits(self, value, size):
        if value.bit_length() > size:
            raise Exception("Size is less than bit representation length of value")

        self.buffer = (self.buffer << size) + value
        self.buffer_size += size

        while self.buffer_size >= 8:
            byte_val = (self.buffer >> (self.buffer_size - 8))
            self.out += bytes([byte_val])
            self.buffer -= byte_val << (self.buffer_size - 8)
            self.buffer_size -= 8

    def write_bytes(self, byte_str, zero_padding=0):
        for i in range(len(byte_str) - 1):
            self.write_bits(byte_str[i], 8)
        if len(byte_str) > 0:
            self.write_bits(byte_str[-1] >> zero_padding, 8 - zero_padding)


    def flush_buffer(self):
        if self.buffer_size > 0:
            zero_padding = 8 - self.buffer_size
            self.out += bytes([self.buffer << zero_padding])
        else:
            return 0
        return zero_padding
    
    def get_bytes(self):
        return self.out
