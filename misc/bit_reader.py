class BitReader():
    def __init__(self, buffer):
        self.buffer = buffer
        self.readPos = 0

    def read_bit(self):
        if self.readPos >= len(self.buffer) * 8:
            raise Exception("Failure reading bit: reached end of buffer")
            
        curr_byte = self.buffer[self.readPos // 8]
        mask = 2 ** (7 - self.readPos % 8)
        bit_value = (curr_byte & mask) >> (7 - (self.readPos % 8))
        self.readPos += 1
        return bit_value

    # 00 00 00 00
    #    ^       
    #    2

    def read_bytes(self, amount=1, as_int=False):
        if as_int:
            res = 0
        else:
            res = b""
        initial_readPos = self.readPos
        for i in range(amount-1, -1, -1):
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
                res += (trunc_left << 8 * i)
            else:
                res += trunc_left.to_bytes(1, "big")

            self.readPos += 8

        return res

    def bits_remaining(self):
        return len(self.buffer) * 8 - self.readPos

