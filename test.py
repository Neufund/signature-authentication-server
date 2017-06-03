import unittest
from signature import *
from challengeResponse import *

def bit_flip(bytes, pos):
    return (int.from_bytes(bytes, 'big') ^ 2**pos).to_bytes(len(bytes), 'big')

class VerifyTest(unittest.TestCase):

    address = '0x29c76e6ad8f28bb1004902578fb108c507be341b'
    message = 'Hello, world!'.encode('utf8')
    hash = bytes.fromhex('b453bd4e271eed985cbab8231da609c4ce0a9cf1f763b6c1594e76315510e0f1')
    signature = bytes.fromhex('90a938f7457df6e8f741264c32697fc52f9a8f867c52dd70713d9d2d472f2e415d9c94148991bbe1f4a1818d1dff09165782749c877f5cf1eff4ef126e55714d1c')


    def test_hash(self):
        hash = message_hash(self.message)
        self.assertEqual(self.hash, hash)

    def test_hash_unicode(self):
        hash = message_hash(self.message.decode('utf8'))
        self.assertEqual(self.hash, hash)

    def test_verify(self):
        self.assertEqual(verify(self.address, self.message, self.signature), True)

    def test_false_address(self):
        address_bytes = bytes.fromhex(self.address[2:])
        for i in range(len(address_bytes) * 8):
            address = bit_flip(address_bytes, i)
            address_enc = '0x' + address.hex()
            self.assertEqual(verify(address_enc, self.message, self.signature), False)

    def test_false_message(self):
        for i in range(len(self.message) * 8):
            message = bit_flip(self.message, i)
            self.assertEqual(verify(self.address, message, self.signature), False)

    def test_false_signature(self):
        for i in range(len(self.signature) * 8):
            signature = bit_flip(self.signature, i)
            self.assertEqual(verify(self.address, self.message, signature), False)

class ChallengeResponseTest(unittest.TestCase):

    address = '0x29c76e6ad8f28bb1004902578fb108c507be341b'

    def test_generate_verify(self):
        challenge = generate_challenge(self.address)
        verify_challenge(self.address, challenge);

    def test_manipulated_challenge(self):
        challenge = generate_challenge(self.address)
        for i in range(len(challenge) * 8):
            manip = bit_flip(challenge, i)
            try:
                verify_challenge(self.address, manip);
                assert False
            except:
                continue

if __name__ == '__main__':
    unittest.main()
