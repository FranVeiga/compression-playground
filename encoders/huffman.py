from io import TextIOWrapper, BufferedWriter
from typing import Dict
from misc.bit_writer import BitWriter
from misc.huffman_tree import HuffmanTree, Node


class HuffmanEncoder:
    """
    Provides utilities to perform huffman encoding on an input
    """

    def encode(self, input: str):
        """
        Huffman encodes a given input. The result will include the encoded file's contents
        as well as the zero-padding size and the search tree. For more information of the
        file format, see HuffmanTree. 
        For getting only the encoded file contents, see encode_data()

        Parameters:
        - input (str): A string with the data to encode.

        Returns:
        - output (bytes): The encoded output.
        """

        frequencies = self.get_char_frequency(input)
        tree = self.construct_search_tree(frequencies)
        code = tree.construct_code()

        encoded_tree, tree_padding = tree.encode()

        data_writer = BitWriter()
        self.encode_data(input, code, data_writer)
        data_padding = data_writer.flush_buffer()

        total_padding = (tree_padding + data_padding) % 8

        out_writer = BitWriter()
        out_writer.write_bits(total_padding, 3)
        out_writer.write_bytes(encoded_tree, zero_padding=tree_padding)
        out_writer.write_bytes(data_writer.get_bytes(), zero_padding=data_padding)
        out_writer.flush_buffer()

        return out_writer.get_bytes()


    def get_char_frequency(self, input: str) -> Dict[str, int]:
        """
        Returns a dictionary with the frequency of each character.

        Parameters:
        - input (str): Input string

        Returns:
        - frequencies (Dict): A dictionary in the form {char: freq}
        """

        dict = {}
        for c in input:
            if dict.get(c):
                dict[c] += 1
            else:
                dict[c] = 1

        return dict

    def construct_search_tree(self, frequencies: Dict):
        """
        Constructs a Huffman search tree from a frequency table.

        Parameters:
        - frequencies (Dict): A dictionary with the frequencies for each character (see get_char_frequency())

        Returns:
        - tree (HuffmanTree): The Huffman search tree
        """

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

    def encode_data(self, input, code, writer):
        """
        Encodes the given data using a Huffman code.

        Parameters:
        - input (str): A string with the data to encode.
        - code (Dict): A dictionary in the form {char: (charcode, bit_size)}
        - writer (BitWriter): Writer to write the encoded output to.
        """

        for char in input:
            charcode, size = code[char]
            writer.write_bits(charcode, size)


