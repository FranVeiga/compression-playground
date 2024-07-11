from misc.bit_reader import BitReader
from misc.bit_writer import BitWriter

##### HUFFMAN COMPRESSED FILE FORMAT #####
# Zero-padding size (3 bits)
# Tree (N bytes)
# Data (N bytes)


class Node:
    """
    Class that represents a node on the Huffman search tree
    """
    def __init__(self, char, weight, childs):
        """
        Creates a new Node.

        Parameters:
            - char (str | None): The char represented by the node. Only present in leaf nodes
            - weight (int): The frequency weight of the node. If -1, the node was constructed
                from decoding an input.
            - childs (Tuple[Node, Node]): The Node's childs
        """
        self.char = char
        self.weight = weight
        self.childs = childs

    def isLeaf(self):
        """
        Returns wether the Node is a leaf node.

        Returns
        - isLeaf (bool)
        """
        return self.childs[0] == None and self.childs[1] == None

    def encode(self, writer: BitWriter):
        """
        Encodes itself and its childs according to the huffman format using recursion.

        Parameters:
        - writer (BitWriter): writer to write the encoded Node to.
        """
        if self.isLeaf():
            writer.write_bits(1, 1)
            writer.write_bits(ord(self.char), 8)
        else:
            writer.write_bits(0, 1)
            self.childs[0].encode(writer)
            self.childs[1].encode(writer)

    @staticmethod
    def decode(reader):
        """
        Decodes a node and its children from a bytestring using recursion.

        Parameters:
            - reader (BitReader): Reader containing the encoded node.

        Returns:
            - node (Node): A new node, with all of its children, if any.
        """

        isLeaf = reader.read_bit()
        if isLeaf:
            char = reader.read_bytes().decode("ascii")
            return Node(char, -1, (None, None))
        else:
            l_child = Node.decode(reader)
            r_child = Node.decode(reader)
            return Node(None, -1, (l_child, r_child))



class HuffmanTree:
    """
    Class which represents a Huffman search tree. The encoded file format
    for a search tree is the following:
    Each bit represents a node. If the bit is 1, then the node is a leaf
    node, and it's followed by 8 bits representing its ascii character.
    If the node bit is 0 however, the node will be followed by its two
    child nodes. For example:

        .    'a'          'b'       'c'   
        0 101100001 0  101100010 101100011
        r
        |----rc-----lc--------------------
        .            |----rc--------lc----

    rc = right child
    lc = left child

    """

    def __init__(self, root: Node):
        """
        Creates a new HuffmanTree instance.

        Parameters:
            - root (Node): The root node.

        Returns:
            - tree (HuffmanTree): A new Huffman search tree.
        """
        self.root = root

    def print_tree(self):
        """
        Prints the tree.
        """

        last_level = 0
        queue = [(self.root, 0)]
        while len(queue) > 0:
            (n, level) = queue.pop(0)
            if (last_level != level):
                print("")
            last_level = level
            char = n.char
            if char == None:
                char = "Inter"
            if char == "\n":
                char = "\\n"
            print(char, end=", ")
            if n.childs[0] != None:
                queue.append((n.childs[0], level + 1))
            if n.childs[1] != None:
                queue.append((n.childs[1], level + 1))
        print("")

    def construct_code(self, inverse=False):
        """
        Constructs the huffman code for each character in the tree.

        Parameters:
            - inverse (bool, default False): Whether to return the code in the
            format {char: (charcode, bit_size)} or {(charcode, bit_size): char}

        Returns:
            - code (Dict): A dict containing the code value and bit_size for each
            character
        """

        code = {}
        path = [] 
        self._add_code(self.root, code, path, inverse)
        return code

    def _add_code(self, node, code, path, inverse):
        """
        Recursive method for adding each character's codes
        """
        if node.isLeaf():
            value = 0
            for i in range(len(path)):
                value += path[len(path) - i - 1] * (2 ** i)
            if not inverse:
                code[node.char] = (value, len(path))
            else:
                code[(value, len(path))] = node.char
            return
        
        self._add_code(node.childs[0], code, path + [0], inverse)
        self._add_code(node.childs[1], code, path + [1], inverse)

    def encode(self):
        """
        Encodes the Huffman tree. See HuffmanTree for details on the format.

        Returns:
            output (Tuple[bytes, int]): The encoded tree and the zero 
            padding at the end of the output bytestring.
        """
        writer = BitWriter()
        self.root.encode(writer)
        zero_padding = writer.flush_buffer()
        return (writer.get_bytes(), zero_padding)

    @staticmethod
    def decode(reader):
        """
        Decodes a binary tree from an encoded input. For details on the format,
        see HuffmanTree.

        Parameters:
            - reader (BitReader): A reader positioned at the start of the tree's data

        Returns:
            - tree (HuffmanTree): The decoded huffman tree.
        """
        return HuffmanTree(Node.decode(reader))


