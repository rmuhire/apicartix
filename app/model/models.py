from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from flask_cors import cross_origin, CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/afr_cartix'

CORS(app)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'no-reply@cartix.io'
app.config['MAIL_PASSWORD'] = 'NoReply=Cartix2016'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(80))
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(25))
    dob = db.Column(db.DateTime)
    user_role = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)
    password = db.Column(db.String(200))
    gender = db.Column(db.String(10))
    job_title = db.Column(db.String(80))
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngo.id'))

    cover = db.relationship('Cover', backref='user', lazy='dynamic')

    def __init__(self, names, username, email, phone, user_role, ngo_id, password, gender, regDate=None):
        self.names = names
        self.username = username
        self.email = email
        self.phone = phone
        self.user_role = user_role
        self.password = password
        self.gender = gender

        if regDate is None:
            self.regDate = datetime.utcnow()
        self.ngo_id = ngo_id



class SavingGroup(db.Model):
    __tablename__ = 'saving_group'
    id = db.Column(db.Integer, primary_key=True)
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
    id = db.Column(db.Integer, primary_key=True)
    saving = db.Column(db.Float)
    borrowing = db.Column(db.Float)
    year = db.Column(db.Integer)
    sg_id =  db.Column(db.Integer, db.ForeignKey('saving_group.id'))

    def __init__(self, saving, borrowing, year, sg_id):
        self.saving = saving
        self.borrowing = borrowing
        self.year = year
        self.sg_id = sg_id

class Ngo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(60))
    telephone = db.Column(db.String(30))
    website = db.Column(db.String(60))
    category = db.Column(db.Integer) # Int NGO 1 : Local NGO : 0
    picture = db.Column(db.String(100))
    address = db.Column(db.String(200))

    user =  db.relationship('User', backref='ngo', lazy='dynamic')

    def __init__(self, name, email, telephone, website, category, picture, address):
        self.name = name
        self.email = email
        self.telephone = telephone
        self.website = website
        self.category = category
        self.picture = picture
        self.address = address

class Sgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer)
    funding_id = db.Column(db.Integer)

    def __init__(self, partner_id, funding_id):
        self.partner_id = partner_id
        self.funding_id = funding_id

class Cover(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    code=db.Column(db.Integer)

    def __init__(self, user_id,code):
        self.user_id=user_id
        self.code=code
