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
