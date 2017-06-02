from bitcoin import privtopub
from ethereum.utils import safe_ord, big_endian_to_int, zpad, bytearray_to_bytestr, int_to_32bytearray, int_to_big_endian
import secp256k1
import rlp
import sha3 as _sha3
sha3 = lambda x: _sha3.keccak_256(x).digest()

# https://github.com/ethereum/wiki/wiki/JavaScript-API#web3ethsign

def parseSignature(signature):
    r = signature[0:32]
    s = signature[32:64]
    v = signature[64:65]
    return v, r, s

def legendreCheck(r):
    SECP256K1P = 2**256 - 4294968273
    # Legendre symbol check; the secp256k1 library does not seem to do this
    xc = r * r * r + 7
    return pow(xc, (SECP256K1P - 1) // 2, SECP256K1P) == 1

def ser_sig(r, s):
    return (zpad(bytearray_to_bytestr(int_to_32bytearray(r)), 32)
        + zpad(bytearray_to_bytestr(int_to_32bytearray(s)), 32))

def ecrecover_to_pub(rawhash, v, r, s, chaincode = 27):
    v = int.from_bytes(v, 'big')
    r = int.from_bytes(r, 'big')
    s = int.from_bytes(s, 'big')
    pk = secp256k1.PublicKey(flags=secp256k1.ALL_FLAGS)
    assert legendreCheck(r)
    recover_sig = pk.ecdsa_recoverable_deserialize(ser_sig(r, s), v - chaincode)
    pk.public_key = pk.ecdsa_recover(rawhash, recover_sig, raw=True)
    return pk.serialize(compressed=False)[1:]

def ecsign(rawhash, key):
    pk = secp256k1.PrivateKey(key, raw=True)
    signature = pk.ecdsa_recoverable_serialize(
        pk.ecdsa_sign_recoverable(rawhash, raw=True)
    )
    signature = signature[0] + bytearray_to_bytestr([signature[1]])
    v = safe_ord(signature[64]) + 27
    r = big_endian_to_int(signature[0:32])
    s = big_endian_to_int(signature[32:64])
    return int_to_big_endian(r), int_to_big_endian(s), int_to_big_endian(v)

def prv_to_pub(privkey):
    return privtopub(privkey)[1:]

def pub_to_addr(pubkey):
    return '0x' + (sha3(pubkey[0:])[12:]).hex()

# https://github.com/ethereumjs/ethereumjs-util/blob/d03528e7da885539cad141c99ea5b88829f73e72/index.js#L345-L348
def message_hash(message):
    message = '\u0019Ethereum Signed Message:\n' + str(len(message)) + message
    return sha3(message.encode('utf8'))

# https://github.com/MetaMask/eth-sig-util/blob/master/test/index.js
test = dict(
    private= bytes.fromhex('4af1bceebf7f3634ec3cff8a2c38e51178d5d4ce585c52d6043e5e2cc3418bb0'),
    public= bytes.fromhex('9e9e45b2ec5f070b4e26f57c7fedf647afa7a03e894789816fbd12fedc5acd79d0dfeea925688e177caccb8f5e09f0c289bbcfc7adb98d76f5f8c5259478903a'),
    address= '0x29c76e6ad8f28bb1004902578fb108c507be341b',
    message= 'Hello, world!',
    hash= bytes.fromhex('b453bd4e271eed985cbab8231da609c4ce0a9cf1f763b6c1594e76315510e0f1'),
    r = bytes.fromhex('90a938f7457df6e8f741264c32697fc52f9a8f867c52dd70713d9d2d472f2e41'),
    s = bytes.fromhex('5d9c94148991bbe1f4a1818d1dff09165782749c877f5cf1eff4ef126e55714d'),
    v = int_to_big_endian(28)
)

# personalSign and extractPublicKey
privatekey = test['private']
pubkey = prv_to_pub(privatekey)
assert pubkey == test['public']

address = pub_to_addr(pubkey)
assert address == test['address']

message = test['message']
hash = message_hash(message)
assert hash == test['hash']

r, s, v = ecsign(hash, privatekey)
print('r = ' + r.hex())
print('s = ' + s.hex())
print('v = ' + v.hex())
assert r == test['r']
assert s == test['s']
assert v == test['v']

p = ecrecover_to_pub(hash, v, r, s, chaincode = 27)
print('p = ' + p.hex())
assert p == test['public']

a = pub_to_addr(p)
print('a = ' + a)
assert a == test['address']
