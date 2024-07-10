from decoders.huffman import HuffmanDecoder
from encoders.huffman import HuffmanEncoder

class Algorithm:
    def __init__(self, encoder, decoder, extension):
        self.encoder = encoder
        self.decoder = decoder
        self.extension = extension

algorithms = {
    "huffman": Algorithm(HuffmanEncoder(), HuffmanDecoder(), ".huff")
}

