import secp256k1
import sha3

def keccak(bytes):
    return sha3.keccak_256(bytes).digest()

def message_hash(message):
    if type(message) != bytes:
        message = message.encode('utf8')
    prefix = '\u0019Ethereum Signed Message:\n' + str(len(message))
    prefix = prefix.encode('utf8')
    return keccak(prefix + message)

def legendre_check(r):
    # Legendre symbol check; the secp256k1 library does not seem to do this
    SECP256K1P = 2**256 - 4294968273
    xc = r * r * r + 7
    return pow(xc, (SECP256K1P - 1) // 2, SECP256K1P) == 1

def ecrecover_to_pub(hash, signature, chaincode = 27):
    assert len(hash) == 32
    assert len(signature) == 65
    assert legendre_check(int.from_bytes(signature[0:32], 'big'))
    hint = signature[-1] - chaincode
    pk = secp256k1.PublicKey(flags=secp256k1.ALL_FLAGS)
    recover_sig = pk.ecdsa_recoverable_deserialize(signature[:-1], hint)
    pk.public_key = pk.ecdsa_recover(hash, recover_sig, raw=True)
    pub = pk.serialize(compressed=False)[1:]
    assert len(pub) == 64
    return pub

def pub_to_address(pubkey):
    return '0x' + (keccak(pubkey[0:])[12:]).hex()

def verify(address, message, signature):
    try:
        hash = message_hash(message)
        pubkey = ecrecover_to_pub(hash, signature)
        return address == pub_to_address(pubkey)
    except:
        return False

test = dict(
    private= bytes.fromhex('4af1bceebf7f3634ec3cff8a2c38e51178d5d4ce585c52d6043e5e2cc3418bb0'),
    public= bytes.fromhex('9e9e45b2ec5f070b4e26f57c7fedf647afa7a03e894789816fbd12fedc5acd79d0dfeea925688e177caccb8f5e09f0c289bbcfc7adb98d76f5f8c5259478903a'),
    address= '0x29c76e6ad8f28bb1004902578fb108c507be341b',
    message= 'Hello, world!',
    hash= bytes.fromhex('b453bd4e271eed985cbab8231da609c4ce0a9cf1f763b6c1594e76315510e0f1'),
    signature = bytes.fromhex('90a938f7457df6e8f741264c32697fc52f9a8f867c52dd70713d9d2d472f2e415d9c94148991bbe1f4a1818d1dff09165782749c877f5cf1eff4ef126e55714d1c')
)

assert verify(test['address'], test['message'], test['signature'])
