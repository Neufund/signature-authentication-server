from datetime import timedelta

AUDIENCE = None
LOGIN_ALGORITHM = "ES512"
PRV_KEY_PATH = "/srv/ec512.prv.pem"
ISSUER = "Neufund"
PRIVATE_ECDSA_KEY = None
LOGIN_TOKEN_LIFE_TIME = timedelta(minutes=30)


def read_keys():
    global PRIVATE_ECDSA_KEY
    with open(PRV_KEY_PATH, "r") as privateKeyFile:
        PRIVATE_ECDSA_KEY = privateKeyFile.read()


read_keys()
