from flask import Flask
from flask import jsonify
from flask import make_response

app = Flask(__name__)


@app.route("/login",methods=['GET'])
def login():
    return jsonify(token="4u6e4o6a4u6")
