import os

from flask import Flask, jsonify, request
from flask_cors import CORS

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
    data = request.get_json()["signature"]
    return data

@app.errorhandler(400)
def bad_request(ex):
    return jsonify({"code": 400, "message": ex.description}), 400

@app.errorhandler(403)
def forbidden(ex):
    return jsonify({"code": 403, "message": ex.description}), 403

@app.errorhandler(404)
def not_found(ex):
    return jsonify({"code": 404, "message": ex.description}), 404

@app.errorhandler(500)
def internal_error(ex):
    return jsonify({"code": 500, "message": ex.description}), 500


if __name__ == '__main__':
    app.run()
