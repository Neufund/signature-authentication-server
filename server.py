import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from auth import *
from challengeResponse import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_mapping(os.environ)
CORS(app)

def validate_address(address):
    assert len(address) == 42
    assert address[:2] == '0x'
    assert address[2:].lower() == bytes.fromhex(address[2:]).hex()
    # TODO: Verify checksum
    return address

def validate_bytes(hex):
    return bytes.fromhex(hex.replace('0x',''))

def validate_jwt():
    try:
        # Authorization: Bearer <token>
        token = request.headers.get("Authorization").split(' ')[1]
        return verify_token(token)
    except:
        abort(401)

@app.route('/api/challenge', methods=['POST'])
def challenge():
    address = validate_address(request.json["address"])
    challenge = generate_challenge(address)
    return  jsonify({"challenge": challenge.hex()})

@app.route('/api/login', methods=['POST'])
def login():
    address = validate_address(request.json["address"])
    challenge = validate_bytes(request.json["challenge"])
    response = validate_bytes(request.json["response"])
    if not verify_response(address, challenge, response):
        abort(403)
    return jsonify({"token": create_token(address)})

@app.route('/api/renew', methods=['POST'])
def renew():
    jwt = validate_jwt()
    address = validate_address(jwt['sub'])
    return jsonify({"token": create_token(address)})

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(406)
@app.errorhandler(500)
@app.errorhandler(501)
@app.errorhandler(502)
@app.errorhandler(504)
@app.errorhandler(505)
def json_error_handler(ex):
    # TODO This does not always get HTMLException with code.
    return jsonify({"code": ex.code, "message": ex.description}), ex.code

if __name__ == '__main__':
    app.run()
