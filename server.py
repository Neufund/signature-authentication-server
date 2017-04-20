import os

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.from_pyfile('config.py')

for key in app.config["REQUIRED_ENV_CONFIG_FIELDS"]:
    if key not in os.environ:
        raise EnvironmentError("Required env variable {} missing".format(key))

app.config.from_mapping(os.environ)


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()["signature"]
    return data


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()["signature"]
    return data


@app.errorhandler(403)
def forbidden(ex):
    return jsonify({"code": 403, "message": ex.description}), 403


@app.errorhandler(404)
def not_found(ex):
    return jsonify({"code": 404, "message": ex.description}), 404


if __name__ == '__main__':
    app.run()
