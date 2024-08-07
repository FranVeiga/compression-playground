class RleEncoder():
    def encode(self, input: bytes):
        out = b""

        if len(input) == 0:
            return out

        curr_byte = input[0]
        count = 1
        

        for i in range(1, len(input)):
            if input[i] == curr_byte:
                if count >= 0xff:
                    out += self.encode_char(curr_byte, count)
                    count = 0
                count += 1
                continue
            else:
                out += self.encode_char(curr_byte, count)
                count = 1
                curr_byte = input[i]
            
        out += self.encode_char(curr_byte, count)

        return out

    def encode_char(self, byte, count):
        out = b""
        out += count.to_bytes(1, byteorder="big")
        out += byte.to_bytes(1, byteorder="big")
        return out
