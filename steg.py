import os
import Image

class RedOnlyStrategy():

    def encode_message(self, image, message):
        message_bits = message_to_bits(message)
        message_bits.reverse()
        width, height = image.size
        for x in range(0, width):
            for y in range(0, height):
                if(len(message_bits) == 0):
                    return
                r,g,b,a = image.getpixel((x,y))
                next_bit = message_bits.pop()
                r = encode_bit(next_bit, r)
                image.putpixel((x,y),(r,g,b,a))

    def decode_message(self, image):
        width, height = image.size
        message_bits = []
        length = 0
        index = 0
        for x in range(0, width):
            for y in range(0, height):
                r,g,b,a = image.getpixel((x,y))
                if(index < 32):
                    message_bits.append(1 if (r&128) == 128 else 0)
                    index += 1
                    if(index == 32):
                        length_bytes = bits_to_bytes(message_bits)
                        length = decode_length(length_bytes)
                else:
                    if(len(message_bits) == (length * 8) + 32):
                        return bits_to_message(message_bits)
                    message_bits.append(1 if (r&128) == 128 else 0)

class Steganographer():

    def __init__(self, strategy, path):
        self.strategy = strategy
        self.path = path

    def encode(self, message):
        im = Image.open(self.path)
        self.strategy.encode_message(im, message)
        path_for_encoded_image = create_path(self.path)
        im.save(path_for_encoded_image)

    def decode(self):
        im = Image.open(self.path)
        message = self.strategy.decode_message(im)
        return message



def set_byte(value):
    return value | 128

def unset_byte(value):
    return value & 127

def byte_to_bits(value):
    value = int(value)
    bits = []
    for x in [128,64,32,16,8,4,2,1]:
        bits.append(1 if (value & x) == x else 0)
    return bits

def bytes_to_bits(bytes):
    return [item for sublist in bytes for item in byte_to_bits(sublist)]

def message_to_bits(message):
    msg_bytes = bytearray(message)
    msg_bits = bytes_to_bits(msg_bytes)
    length_bytes  = encode_length(len(msg_bytes))
    length_bits = bytes_to_bits(length_bytes)
    return length_bits + msg_bits

def bits_to_byte(bits):
    byte = 0
    bit_values = [128,64,32,16,8,4,2,1]
    for i in range(0,8):
        if (bits[i] == 1):
            byte |= bit_values[i]
    return byte

def utf8(byte):
    return bytearray([byte]).decode('utf8')

def bits_to_message(bits):
    message = ''
    step = 8
    for i in range(8*4, len(bits), step):
        sub_bits = bits[i:i+step]
        message += utf8(bits_to_byte(sub_bits))
    return message

def bits_to_bytes(bits):
    bytes = [];
    for i in range(0,len(bits), 8):
        bytes.append(bits_to_byte(bits[i:i+8]))
    return bytes

def encode_bit(bit, byte):
    if bit == 1:
        return set_byte(byte)
    else:
        return unset_byte(byte)

def pad_front(array, total):
    copy = array
    for i in range(0,total-len(array)):
        copy = [0]+copy    

    return copy

def encode_length(length):
    encodedBytes = [];
    x = length
    encodedByte = x % 128
    x = int(x / 128)
    if ( x > 0 ):
        encodedByte = encodedByte | 128
    encodedBytes = [encodedByte] +  encodedBytes 
    while ( x > 0 ):
        encodedByte = x % 128
        x = x / 128
        if ( x > 0 ):
            encodedByte = encodedByte | 128
        encodedBytes = [encodedByte] + encodedBytes

    return pad_front(encodedBytes, 4)

def decode_length(bytes):
    multiplier = 1
    value = 0
    encodedByte = bytes.pop()
    value += (encodedByte & 127) * multiplier
    multiplier *= 128
    if (multiplier > 128*128*128):
        raise Error('Malformed Length')
    while ((encodedByte & 128) != 0):
        encodedByte = bytes.pop()
        value += (encodedByte & 127) * multiplier
        multiplier *= 128
        if (multiplier > 128*128*128):
            raise Error('Malformed Length')
    return value

def create_path(path):
    resolved_path = os.path.abspath(path)
    dirname = os.path.dirname(resolved_path)
    filename,ext = os.path.splitext(resolved_path)
    new_path = os.path.join(dirname,filename+'.encoded'+ext)
    return new_path
