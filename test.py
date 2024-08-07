from encoders.rle import *
from decoders.rle import *

encoder = RleEncoder()
decoder = RleDecoder()

test_string_dec = b"aaabbbccc"
test_string_enc = b"\x03a\x03b\x03c"

decoded = decoder.decode(test_string_enc)

print(decoded)
print(decoded == test_string_dec)

