from misc.bit_reader import BitReader
from misc.huffman_tree import HuffmanTree


class HuffmanDecoder():
    """
    Provides utilities for handling input compressed with huffman encoding
    """

    def decode(self, input: bytes):
        """
        Performs huffman decoding on a byte input. 
        The input must be provided in full format, including the search tree and the two 'size' bytes at 
        the beginning (see HuffmanTree for more information on the format). To decode the raw data using
        a search tree, see parse_data())

        Parameters:
        - input (bytes): Encoded input in bytestring format.

        Returns:
        - output (bytes): Decoded output in bytestring format.
        """

        reader = BitReader(input)
        data_padding = 0
        for _ in range(3):
            data_padding = data_padding << 1 + reader.read_bit()

        # Get the tree out from the bit stream
        tree = HuffmanTree.decode(reader)

        # Parse the remaining data - out file contents
        out = self.parse_data(reader, tree, data_padding)

        return out

    def parse_data(self, reader, tree, padding):
        """
        Performs huffman decoding on a bytestring given a search tree.

        Parameters:
            - reader (BitReader): reader positioned at the start of the encoded file's data.
            - tree (HuffmanTree): the search tree to use for decoding.
            - padding (int): zero-padding at the end of the file's data

        Returns:
            - output (bytes): Decoded output as a bytestring.
            
        """

        out = b""
        curr_node = tree.root

        while reader.bits_remaining() > padding:
            # if somehow we get to a bit sequence not represented in the tree
            if curr_node == None:
                raise Exception("Unknown bit sequence")

            if curr_node.isLeaf():
                out += curr_node.char.encode()
                curr_node = tree.root
                continue

            bit = reader.read_bit()
            curr_node = curr_node.childs[bit] # 0 is left child, 1 is right

        return out
        

