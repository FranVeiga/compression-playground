class RleDecoder():
    def decode(self, input: bytes):
        out = b""
        for (count, char) in self.read_pairs(input):
            out += char.to_bytes(1, byteorder="big") * count

        return out
        

    def read_pairs(self, input: bytes):
        for i in range(len(input) // 2):
            yield (input[i * 2], input[i * 2 + 1])
