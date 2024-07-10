from encoders.huffman import HuffmanEncoder

class Algorithm:
    def __init__(self, encoder, extension):
        self.encoder = encoder
        self.extension = extension

algorithms = {
    "huffman": Algorithm(HuffmanEncoder(), ".huff")
}

