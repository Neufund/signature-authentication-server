import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import auth

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_mapping(os.environ)
CORS(app)


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()["signature"]
    return data


@app.route('/api/login', methods=['POST'])
def login():
    address = request.get_json()["address"]
    data = request.get_json()["signature"]
    return auth.sign_login_credentials({"sub": address})


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
    return jsonify({"code": ex.code, "message": ex.description}), ex.code

if __name__ == '__main__':
    app.run()
