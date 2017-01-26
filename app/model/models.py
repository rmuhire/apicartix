from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import cross_origin, CORS
from flask_mail import Mail, Message


app = Flask(__name__)

CORS(app)

db = SQLAlchemy(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://muhireremy:8@localhost/afr_cartix'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:afr_cartix@2156@localhost/afr_cartix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'rmuhire'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEFAULT_SENDER'] = 'Cartix Team'
app.config['MAIL_USERNAME'] = 'no-reply@cartix.io'
app.config['MAIL_PASSWORD'] = 'NoReply=Cartix2016'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(80))
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(25))
    dob = db.Column(db.DateTime)
    user_role = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)
    password = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    update_key = db.Column(db.String(240))
    job_title = db.Column(db.String(80))
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngo.id'))

    files = db.relationship('Files', backref='user', lazy='dynamic')

    def __init__(self, names, username, email, phone, user_role, ngo_id, password, gender, update_key, regDate=None):
        self.names = names
        self.username = username
        self.email = email
        self.phone = phone
        self.user_role = user_role
        self.password = password
        self.gender = gender
        self.update_key = update_key

        if regDate is None:
            regDate = datetime.utcnow()
        self.regDate = regDate

        self.ngo_id = ngo_id


class SavingGroup(db.Model):
    __tablename__ = 'saving_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    year = db.Column(db.Integer)
    member_female = db.Column(db.Integer)
    member_male = db.Column(db.Integer)
    sector_id = db.Column(db.Integer)
    sector_name = db.Column(db.String(100))
    district_name = db.Column(db.String(100))
    regDate = db.Column(db.DateTime)

    Amount = db.relationship('Amount', backref='saving_group', lazy='dynamic')

    def __init__(self, name, year, member_female, member_male, sector_id, sector_name, district_name, regDate = None):
        self.name = name,
        self.year = year
        self.member_female = member_female
        self.member_male = member_male
        self.sector_id = sector_id
        self.sector_name = sector_name
        self.district_name = district_name
        if regDate is None:
            self.regDate = datetime.utcnow()


class Amount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saving = db.Column(db.Float)
    borrowing = db.Column(db.Float)
    year = db.Column(db.Integer)
    sg_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'))

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

    user = db.relationship('User', backref='ngo', lazy='dynamic')

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
    sg_id = db.Column(db.Integer)

    def __init__(self, partner_id, funding_id, sg_id):
        self.partner_id = partner_id
        self.funding_id = funding_id
        self.sg_id = sg_id


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(175))
    saved = db.Column(db.String(175))
    filename = db.Column(db.String(150))
    regDate = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, original, saved, filename, status, user_id, regDate=None):
        self.original = original
        self.saved = saved
        self.filename = filename
        self.status = status
        self.user_id = user_id
        if regDate is None:
            regDate = datetime.utcnow()
        self.regDate = regDate


class Province(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(10))
    keyword = db.Column(db.String(150))

    province = db.relationship('District', backref='province', lazy='dynamic')

    def __init__(self, id, name, code, keyword):
        self.id = id
        self.name = name
        self.code = code
        self.keyword = keyword


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(10))
    province_code = db.Column(db.String(10))
    province_id = db.Column(db.Integer, db.ForeignKey('province.id'))

    district = db.relationship('Sector', backref='district', lazy='dynamic')
    bank_agent_district = db.relationship('BankAgent', backref='district', lazy='dynamic')
    telco_agent_district = db.relationship('TelcoAgent', backref='district', lazy='dynamic')

    def __init__(self, id, name, code, province_code, province_id):
        self.id = id
        self.name = name
        self.code = code
        self.province_code = province_code
        self.province_id = province_id


class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100))
    district_code = db.Column(db.String(10))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))

    sector_financial = db.relationship('Financial', backref='sector', lazy='dynamic')
    sector_population = db.relationship('Population', backref='sector', lazy='dynamic')

    def __init__(self, id, name, code, district_code, district_id):
        self.id = id
        self.name = name
        self.code = code
        self.district_code = district_code
        self.district_id = district_id


class Financial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100))
    financial_name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))

    def __init__(self, id, branch_name, financial_name, sector_id):
        self.id = id
        self.branch_name = branch_name
        self.financial_name = financial_name
        self.sector_id = sector_id


class BankAgent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distribution = db.Column(db.Integer)
    year = db.Column(db.Integer)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))

    def __init__(self, distribution, district_id):
        self.distribution = distribution
        self.district_id = district_id


class TelcoAgent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distribution = db.Column(db.Integer)
    year = db.Column(db.Integer)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))

    def __init__(self, distribution, district_id):
        self.distribution = distribution
        self.district_id = district_id


class Population(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    male = db.Column(db.Integer)
    female = db.Column(db.Integer)
    year = db.Column(db.Integer)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))

    def __init__(self, male, female, sector_id):
        self.male = male
        self.female = female
        self.sector_id = sector_id











