import hmac
import signature
from os import urandom
from datetime import datetime, timedelta

'''Generate a unique hmac key on start'''
hmac_key = urandom(32)

def generate_mac(msg):
    return hmac.new(hmac_key, msg=msg, digestmod='sha384').digest()

def verify_mac(msg, mac):
    return hmac.compare_digest(generate_mac(msg), mac)

def add_mac(msg):
    return msg + generate_mac(msg)

def strip_mac(msg):
    assert verify_mac(msg[:-48], msg[-48:])
    return msg[:-48]

def generate_challenge(address, ttl=60):
    address = bytes.fromhex(address[2:])
    expiry = datetime.utcnow() + timedelta(seconds=ttl)
    timestamp = int(expiry.timestamp()).to_bytes(4, 'big')
    return add_mac(address + timestamp)

def verify_challenge(address, challenge):
    msg = strip_mac(challenge)
    expiry = datetime.fromtimestamp(int.from_bytes(msg[20:24], 'big'))
    assert msg[:20] == bytes.fromhex(address[2:])
    assert expiry > datetime.utcnow()

def verify_response(address, challenge, response):
    try:
        verify_challenge(address, challenge)
        assert signature.verify(address, challenge, response)
    except e:
        return False
    finally:
        return True
