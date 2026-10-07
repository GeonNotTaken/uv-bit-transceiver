def char_to_bits(char, nbits=8):
    """Encode a single character as a sequence of nbit binary values
    representing its numeric code, starting with the least-significant bit.
    """
    value = ord(char)
    binary = bin(value)
#     print(value)
    binary = ''
    for i in range(nbits):
        binary += str((value >> i) & 1)
    return binary

# print(char_to_bits('A'))

def bits_to_char(bits, nbits=8):
    """Decode a sequence of nbit binary values back to a character.
    """
    # Reverse the bits since they're stored LSB-first
    decimal = int(bits[::-1], 2)  # [::-1] reverses the string
    return chr(decimal)

test = char_to_bits('Z')
test2 = bits_to_char(test)
print(test2)  # Should print 'A'