from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/afr_cartix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

import datetime


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/afr_cartix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class SavingGroup(db.Model):
    __tablename__ = 'saving_group'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    member_female = db.Column(db.Integer)
    member_male = db.Column(db.Integer)
    sector_id = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)

    Amount = db.relationship('Amount', backref='saving_group', lazy='dynamic')

    def __init__(self, name, year, member_female, member_male, sector_id, regDate = None):
        self.name = name,
        self.year = year
        self.member_female = member_female
        self.member_male = member_male
        self.sector_id = sector_id
        if regDate is None:

                regDate = datetime.utcnow()

        self.regDate = regDate

class Amount(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    saving = db.Column(db.Float)
    borrowing = db.Column(db.Float)
    year = db.Column(db.Integer)
    sg_id =  db.Column(db.Integer, db.ForeignKey('saving_group.id'))

    def __init__(self, saving, borrowing, year, sg_id):
        self.saving = saving
        self.borrowing = borrowing
        self.year = year
        self.sg_id = sg_id


class Funding(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(60))
    username = db.Column(db.String(30))
    cp_name = db.Column(db.String(60))
    cp_email = db.Column(db.String(60), unique = True)
    cp_telephone = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(50))
    sgs = db.relationship('Sgs', backref='funding', lazy='dynamic')

    def __init__(self, name, email, username, cp_name, cp_email, cp_telephone, password):
        self.name = name
        self.email = email
        self.username = username
        self.cp_name = cp_name
        self.cp_email = cp_email
        self.cp_telephone = cp_telephone
        self.password = password


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(60))
    username = db.Column(db.String(30))
    cp_name = db.Column(db.String(60))
    cp_email = db.Column(db.String(60), unique=True)
    cp_telephone = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))

    sgs = db.relationship('Sgs', backref='partner', lazy='dynamic')

    def __init__(self, name, email, username, cp_name, cp_email, cp_telephone,password):
        self.name = name
        self.email = email
        self.username = username
        self.cp_name = cp_name
        self.cp_email = cp_email
        self.cp_telephone = cp_telephone
        self.password = password

class Sgs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    funding_id =  db.Column(db.Integer, db.ForeignKey('funding.id'))

    def __init__(self, partner_id, funding_id):
        self.partner_id = partner_id
        self.funding_id = funding_id
