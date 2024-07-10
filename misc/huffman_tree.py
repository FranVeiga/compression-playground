from misc.byte_writer import ByteWriter


class Node:
    def __init__(self, char, weight, childs):
        self.char = char
        self.weight = weight
        self.childs = childs

    def isLeaf(self):
        return self.childs[0] == None and self.childs[1] == None

    def encode(self, writer: ByteWriter):
        if self.isLeaf():
            writer.write_bits(1, 1)
            writer.write_bits(ord(self.char), 8)
        else:
            writer.write_bits(0, 1)
            self.childs[0].encode(writer)
            self.childs[1].encode(writer)



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

    def encode(self):
        writer = ByteWriter()
        self.root.encode(writer)
        zero_padding = writer.flush_buffer()
        return (writer.get_bytes(), zero_padding)


