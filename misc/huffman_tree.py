from misc.bit_reader import BitReader
from misc.bit_writer import BitWriter


class Node:
    def __init__(self, char, weight, childs):
        self.char = char
        self.weight = weight
        self.childs = childs

    def isLeaf(self):
        return self.childs[0] == None and self.childs[1] == None

    def encode(self, writer: BitWriter):
        if self.isLeaf():
            writer.write_bits(1, 1)
            writer.write_bits(ord(self.char), 8)
        else:
            writer.write_bits(0, 1)
            self.childs[0].encode(writer)
            self.childs[1].encode(writer)

    @staticmethod
    def decode(reader):
        isLeaf = reader.read_bit()
        if isLeaf:
            char = reader.read_bytes().decode("ascii")
            return Node(char, -1, (None, None))
        else:
            l_child = Node.decode(reader)
            r_child = Node.decode(reader)
            return Node(None, -1, (l_child, r_child))



class HuffmanTree:
    def __init__(self, root: Node):
        self.root = root

    def print_tree(self):
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
        code = {}
        path = [] 
        self._add_code(self.root, code, path, inverse)
        return code

    def _add_code(self, node, code, path, inverse):
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
        writer = BitWriter()
        self.root.encode(writer)
        zero_padding = writer.flush_buffer()
        return (writer.get_bytes(), zero_padding)

    @staticmethod
    def decode(input: bytes):
        reader = BitReader(input)
        return HuffmanTree(Node.decode(reader))


