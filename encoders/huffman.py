from io import TextIOWrapper, BufferedWriter
from typing import Dict
from misc.byte_writer import ByteWriter
from misc.huffman_tree import HuffmanTree, Node

##### HUFFMAN COMPRESSED FILE FORMAT #####
# Tree size / Zero-padding size (2 bytes --> 13 bits + 3 bits)
# Tree (N bytes)
# Data (N bytes)


class HuffmanEncoder:
    def encode(self, input: str):
        frequencies = self.get_char_frequency(input)
        tree = self.construct_search_tree(frequencies)
        code = self.construct_code(tree)

        encoded_tree, tree_padding = tree.encode()
        tree_size = len(encoded_tree) * 8 - tree_padding

        data_writer = ByteWriter()
        for char in input:
            charcode, size = code[char]
            data_writer.write_bits(charcode, size)
        data_padding = data_writer.flush_buffer()
        print("data padding: " + str(data_padding))
        data = ''.join("{0:b}".format(i) for i in data_writer.get_bytes())
        print(data)

        total_padding = (tree_padding + data_padding) % 8

        out_writer = ByteWriter()
        out_writer.write_bits(tree_size, 13)
        out_writer.write_bits(total_padding, 3)
        out_writer.write_bytes(encoded_tree, zero_padding=tree_padding)
        out_writer.write_bytes(data_writer.get_bytes())
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

    def construct_code(self, tree):
        code = {}
        path = [] 
        self._add_code(tree.root, code, path)
        return code

    def _add_code(self, node, code, path):
        if node.isLeaf():
            value = 0
            for i in range(len(path)):
                value += path[len(path) - i - 1] * (2 ** i)
            code[node.char] = (value, len(path))
            return
        
        self._add_code(node.childs[0], code, path + [0])
        self._add_code(node.childs[1], code, path + [1])

