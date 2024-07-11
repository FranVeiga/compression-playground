class BitWriter:
    """
    Class that provides utilities to write bits to a buffer.
    """

    def __init__(self):
        """
        Creates a new BitWriter instance.

        Returns:
        - writer (BitWriter): New BitWriter instance
        """

        self.out = b""
        self.buffer = 0
        self.buffer_size = 0

    def write_bits(self, value, size):
        """
        Writes a determined amount of bits to the buffer. 'size' must not be less
        that the bit representation of 'value', otherwise this function will raise
        an exception.
        If 'size' is bigger than the bit representation of 'value' the bits written
        will be left-padded with zeros.

        Parameters:
        - value (int): the numeric value of the bits to be written
        - size (int): the amount of bits to be written
        """

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
        """
        Writes bytes to the buffer.

        Parameters:
            - zero_padding (int, default 0): The amount of padding of the last byte
            in 'byte_str', which will not be written to the buffer.
        """

        for i in range(len(byte_str) - 1):
            self.write_bits(byte_str[i], 8)
        if len(byte_str) > 0:
            self.write_bits(byte_str[-1] >> zero_padding, 8 - zero_padding)


    def flush_buffer(self):
        """
        Writes the remaining bits to the buffer. Will right-pad with zeros to complete 
        the last byte.

        Returns:
            - padding: The amount of padding (bits) used to complete the last byte
        """
        if self.buffer_size > 0:
            zero_padding = 8 - self.buffer_size
            self.out += bytes([self.buffer << zero_padding])
        else:
            return 0
        return zero_padding
    
    def get_bytes(self):
        return self.out
