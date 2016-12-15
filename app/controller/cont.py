from flask import Flask, jsonify, request,render_template
from flask_bcrypt import Bcrypt
import templates

app = Flask(__name__)

bcrypt = Bcrypt(app)


def changePass(json_data,pas):
    pwd_hash = bcrypt.generate_password_hash(pas)
    pas=pwd_hash
    return pas
