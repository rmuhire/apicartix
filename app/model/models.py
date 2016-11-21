from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://muhireremy:8@localhost/afr_cartix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class SavingGroup(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    member_female = db.Column(db.Integer)
    member_male = db.Column(db.Integer)
    sector_id = db.Column(db.Integer)

    def __init__(self, name, year, member_female, member_male, sector_id):
        self.name = name,
        self.year = year
        self.member_female = member_female
        self.member_male = member_male
        self.sector_id = sector_id

class Amount(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    saving = db.Column(db.Float)
    borrowing = db.Column(db.Float)
    year = db.Column(db.Integer)
    sg_id =  db.Column(db.Integer)

    