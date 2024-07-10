from io import TextIOWrapper, BufferedWriter
from typing import Dict
from misc.bit_writer import BitWriter
from misc.huffman_tree import HuffmanTree, Node

##### HUFFMAN COMPRESSED FILE FORMAT #####
# Tree size / Zero-padding size (2 bytes --> 13 bits + 3 bits)
# Tree (N bytes)
# Data (N bytes)


class HuffmanEncoder:
    def encode(self, input: str):
        frequencies = self.get_char_frequency(input)
        tree = self.construct_search_tree(frequencies)
        code = tree.construct_code()

        encoded_tree, tree_padding = tree.encode()
        tree_size = len(encoded_tree) * 8 - tree_padding

        data_writer = BitWriter()
        last_char = ""
        for char in input:
            last_char = char
            charcode, size = code[char]
            data_writer.write_bits(charcode, size)

        data_padding = data_writer.flush_buffer()

        total_padding = (tree_padding + data_padding) % 8

        out_writer = BitWriter()
        out_writer.write_bits(tree_size, 13)
        out_writer.write_bits(total_padding, 3)
        out_writer.write_bytes(encoded_tree, zero_padding=tree_padding)
        out_writer.write_bytes(data_writer.get_bytes(), zero_padding=data_padding)
        out_writer.flush_buffer()

        return out_writer.get_bytes()


    def get_char_frequency(self, input: str) -> Dict[str, int]:
        dict = {}
        for c in input:
            if dict.get(c):
                dict[c] += 1
            else:
                dict[c] = 1

        return dict

    def construct_search_tree(self, frequencies: Dict):
        nodes = [Node(k, v, (None, None)) for (k, v) in frequencies.items()]
        nodes.sort(key=lambda n: n.weight)
        
        while len(nodes) > 1:
            left = nodes.pop(0)
            right = nodes.pop(0)
            head = Node(None, left.weight + right.weight, (left, right))
            nodes.append(head)
            nodes.sort(key=lambda n: n.weight)

        tree = HuffmanTree(nodes[0])
        return tree


