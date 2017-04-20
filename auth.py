from datetime import datetime

import jwt


def _get_claims(audience, ttl):
    from server import app
    return {
        # Expiration Time Claim
        'exp': datetime.utcnow() + ttl,
        # Not Before Time Claim
        'nbf': datetime.utcnow(),
        # Issuer Claim
        'iss': app.config['ISSUER'],
        # Audience Claim
        'aud': audience,
        # Issued At Claim
        'iat': datetime.utcnow()
    }


def sign_login_credentials(data):
    from server import app
    payload = {**data,
               **_get_claims(app.config['MS2_AUDIENCE'], app.config["LOGIN_TOKEN_LIFE_TIME"])}
    return jwt.encode(payload, app.config['PRIVATE_ECDSA_KEY'],
                      algorithm=app.config['LOGIN_ALGORITHM'])
