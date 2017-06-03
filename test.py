import unittest
from signature import *

class VerifyTest(unittest.TestCase):

    def test_hash(self):
        message = 'Hello, world!'
        ehash = bytes.fromhex('b453bd4e271eed985cbab8231da609c4ce0a9cf1f763b6c1594e76315510e0f1')
        hash = message_hash(message)
        self.assertEqual(hash, ehash)

    def test_verify(self):
        address = '0x29c76e6ad8f28bb1004902578fb108c507be341b'
        message = 'Hello, world!'
        signature = bytes.fromhex('90a938f7457df6e8f741264c32697fc52f9a8f867c52dd70713d9d2d472f2e415d9c94148991bbe1f4a1818d1dff09165782749c877f5cf1eff4ef126e55714d1c')
        self.assertEqual(verify(address, message, signature), True)

if __name__ == '__main__':
    unittest.main()
