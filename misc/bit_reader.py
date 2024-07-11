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
        self._read_pos = 0

    def read_bit(self):
        """
        Reads a bit from the stream.

        Returns:
        - bit (Int): Can be either zero or one
        """

        if self._read_pos >= len(self.buffer) * 8:
            raise Exception("Failure reading bit: reached end of buffer")
            
        curr_byte = self.buffer[self._read_pos // 8]
        # Get the value of the bit at readPos
        bit_value = (curr_byte >> (7 - (self._read_pos % 8))) & 1
        self._read_pos += 1
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
        initial_read_pos = self._read_pos
        for _ in range(amount):
            if self.bits_remaining() < 8:
                self._read_pos = initial_read_pos
                raise Exception("Failure reading byte: reached end of buffer")
            start_byte_pos = self._read_pos // 8
            end_byte_pos = (self._read_pos + 7) // 8 
            # gets one or two bytes depending on self._read_pos
            bytes_slice = self.buffer[start_byte_pos:end_byte_pos+1]
            if len(bytes_slice) == 1:
                ret_value = bytes_slice[0]
            else:
                # if the wanted byte crosses byte boundaries, extract it
                bytes_value = (bytes_slice[0] << 8) + bytes_slice[1]
                start_bit_pos = self._read_pos % 8
                ret_value = (bytes_value >> (8 - start_bit_pos)) & 0xff

            if as_int:
                res = res << 8 + ret_value
            else:
                res += ret_value.to_bytes(1, "big")

            self._read_pos += 8

        return res

    def bits_remaining(self):
        """
        Returns the amount of remaining bits in the stream.

        Returns:
        - bits (int): Amount of remaining bits.
        """
        return len(self.buffer) * 8 - self._read_pos

