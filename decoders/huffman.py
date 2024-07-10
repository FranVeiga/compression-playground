from misc.bit_reader import BitReader
from misc.huffman_tree import HuffmanTree


class HuffmanDecoder():
    def decode(self, input: bytes):
        reader = BitReader(input)
        header = reader.read_bytes(2, as_int=True)
        tree_size = header >> 3
        data_padding = header - (tree_size << 3)
        tree_data = self.read_tree_data(reader, tree_size)

        tree = HuffmanTree.decode(tree_data)
        code = tree.construct_code(inverse=True)

        out = self.parse_data(reader, code, data_padding)

        return out


    def read_tree_data(self, reader, tree_size):
        tree_data = reader.read_bytes(tree_size // 8)
        last_byte = 0
        for _ in range(tree_size % 8):
            last_byte = (last_byte << 1) + reader.read_bit()
        last_byte = last_byte << (8 - (tree_size % 8))
        tree_data += last_byte.to_bytes(1, "big")
        return tree_data

    def parse_data(self, reader, code, padding):
        out = b""
        buffer = 0
        buf_size = 0
        while reader.bits_remaining() > padding:
            buffer = (buffer << 1) + reader.read_bit()
            buf_size += 1
            char = code.get((buffer, buf_size))
            if char:
                out += char.encode()
                buffer = 0
                buf_size = 0
        return out




        

