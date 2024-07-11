class BitReader():
    """
    Provides utilities to read bits from a bytestring in a streaming fashion.
    """

    def __init__(self, buffer):
        """
        Creates a new BitReader instance.

        Parameters:
        - buffer (bytes): The bytes input to be read.

        Returns:
        - reader (BitReader): A new BitReader instance.
        """

        self.buffer = buffer
        self.readPos = 0

    def read_bit(self):
        """
        Reads a bit from the stream.

        Returns:
        - bit (Int): Can be either zero or one
        """

        if self.readPos >= len(self.buffer) * 8:
            raise Exception("Failure reading bit: reached end of buffer")
            
        curr_byte = self.buffer[self.readPos // 8]
        mask = 2 ** (7 - self.readPos % 8)
        bit_value = (curr_byte & mask) >> (7 - (self.readPos % 8))
        self.readPos += 1
        return bit_value

    def read_bytes(self, amount=1, as_int=False):
        """
        Reads bytes from the stream.

        Parameters:
        - amount (int, default 1): The amount of bytes to be read.
        - as_int (bool, default False): Whether to return the output as an integer or as a bytestring.

        Returns:
        - bytes (bytes | int): the read bytes.
        """

        if as_int:
            res = 0
        else:
            res = b""
        initial_readPos = self.readPos
        for _ in range(amount):
            if self.bits_remaining() < 8:
                self.readPos = initial_readPos
                raise Exception("Failure reading byte: reached end of buffer")
            byte_pos = self.readPos // 8
            two_bytes = self.buffer[byte_pos:byte_pos+2]
            bytes_value = (two_bytes[0] << 8) + two_bytes[1]

            bit_pos = self.readPos % 8
            trunc_right = bytes_value >> (8 - bit_pos)
            trunc_left = trunc_right - ((trunc_right >> 8) << 8)

            if as_int:
                res = res << 8 + trunc_left
            else:
                res += trunc_left.to_bytes(1, "big")

            self.readPos += 8

        return res

    def bits_remaining(self):
        """
        Returns the amount of remaining bits in the stream.

        Returns:
        - bits (int): Amount of remaining bits.
        """
        return len(self.buffer) * 8 - self.readPos

