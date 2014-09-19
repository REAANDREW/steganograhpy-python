import unittest
from steg import *

class TestBitsAndBytesUtilities(unittest.TestCase):

    def test_set_a_byte(self):
        byte = 1;
        self.assertEqual(set_byte(byte),129)

    def test_unset_a_byte(self):
        byte = 129
        self.assertEqual(unset_byte(byte), 1)

    def test_byte_to_bits(self):
        byte = 129
        self.assertEqual(byte_to_bits(byte), [1,0,0,0,0,0,0,1])

    def test_message_to_bits(self):
        message = 'hello'
        bits = message_to_bits(message)
        #msgbits + (numberOfBytesForLength + numberOfBitsPerByte
        self.assertEqual(len(bits), 40 + (4 * 8))
        #Remove the length bits from the beginning
        bits = bits[32:]
        self.assertEqual(utf8(bits_to_byte(bits[0:8])), 'h')
        self.assertEqual(utf8(bits_to_byte(bits[8:16])), 'e')
        self.assertEqual(utf8(bits_to_byte(bits[16:24])), 'l')
        self.assertEqual(utf8(bits_to_byte(bits[24:32])), 'l')
        self.assertEqual(utf8(bits_to_byte(bits[32:40])), 'o')

    def test_bits_to_byte(self):
        bits = [1,0,0,0,0,0,0,1];
        self.assertEqual(bits_to_byte(bits), 129)

    def test_bits_to_message(self):
        message = 'hello'
        bits = message_to_bits(message)
        self.assertEqual(bits_to_message(bits), message)

    def test_encode_bit(self):
        bit = 1
        byte = 1
        self.assertEqual(encode_bit(bit, byte), 129)
        bit = 0
        byte = 255
        self.assertEqual(encode_bit(bit, byte), 127)

    def test_encode_length(self):
        number = 128
        self.assertEqual(encode_length(number), [0,0,1,128])

    def test_decode_length(self):
        bytes = [0,1,128,128];
        self.assertEquals(decode_length(bytes), 128*128)

    def test_bits_to_bytes(self):
        bits = ([0]*32)+[0,0,0,0,1,0,1,1]
        self.assertEquals(len(bits_to_bytes(bits)), 5)

if __name__ == '__main__':
    unittest.main()
