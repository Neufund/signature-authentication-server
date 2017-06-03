from datetime import timedelta

AUDIENCE = 'web3'
LOGIN_ALGORITHM = "ES512"
PRV_KEY_PATH = "/srv/ec512.prv.pem"
PUB_KEY_PATH = "/srv/ec512.pub.pem"
ISSUER = "Neufund"
PRIVATE_ECDSA_KEY = None
PUBLIC_ECDSA_KEY = None
CHALLENGE_LIFE_TIME = timedelta(seconds=60)
LOGIN_TOKEN_LIFE_TIME = timedelta(minutes=30)


def read_keys():
    global PRIVATE_ECDSA_KEY
    with open(PRV_KEY_PATH, "r") as keyFile:
        PRIVATE_ECDSA_KEY = keyFile.read()
    global PUBLIC_ECDSA_KEY
    with open(PUB_KEY_PATH, "r") as keyFile:
        PUBLIC_ECDSA_KEY = keyFile.read()


read_keys()
