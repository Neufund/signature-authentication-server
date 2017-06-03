from datetime import datetime
import jwt

def create_token(subject):
    from server import app
    return jwt.encode(
        {
            'sub': subject,
            'exp': datetime.utcnow() + app.config["LOGIN_TOKEN_LIFE_TIME"],
            'nbf': datetime.utcnow(),
            'iss': app.config['ISSUER'],
            'aud': app.config['AUDIENCE'],
            'iat': datetime.utcnow()
        },
        app.config['PRIVATE_ECDSA_KEY'],
        algorithm=app.config['LOGIN_ALGORITHM']
    ).decode('ascii')

def verify_token(token):
    from server import app
    return jwt.decode(
        token,
        key=app.config['PUBLIC_ECDSA_KEY'],
        audience=app.config['AUDIENCE'],
        algorithms=[app.config['LOGIN_ALGORITHM']],
        verify=True,
    )
