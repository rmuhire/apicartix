from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://muhireremy:8@localhost/afr_cartix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class SavingGroup(db.Model):
    sg_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    menber_female = db.Column(db.Integer)
    menber_male = db.Column(db.Integer)
    sector_id = db.Column(db.Integer)

    