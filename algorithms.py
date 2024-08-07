from decoders.huffman import HuffmanDecoder
from encoders.huffman import HuffmanEncoder
from encoders.rle import RleEncoder
from decoders.rle import RleDecoder

class Algorithm:
    def __init__(self, encoder, decoder, extension):
        self.encoder = encoder
        self.decoder = decoder
        self.extension = extension

algorithms = {
    "huffman": Algorithm(HuffmanEncoder(), HuffmanDecoder(), ".huff"),
    "rle": Algorithm(RleEncoder(), RleDecoder(), ".rle")
}

