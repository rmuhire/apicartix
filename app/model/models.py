from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import cross_origin, CORS
from flask_mail import Mail, Message


app = Flask(__name__)

CORS(app)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://muhireremy:8@localhost/afr_cartix'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:afr_cartix@2156@localhost/afr_cartix'
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
    name = db.Column(db.String(100))
    year_of_creation = db.Column(db.Integer)
    member_female = db.Column(db.Integer)
    member_male = db.Column(db.Integer)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    sg_status = db.Column(db.String(100))
    saving = db.Column(db.Float)
    borrowing = db.Column(db.Float)
    year = db.Column(db.Integer)
    partner_id = db.Column(db.Integer, db.ForeignKey('ngo.id'))
    funding_id = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)

    def __init__(self, name, year_of_creation, member_female, member_male, sector_id, sg_status, saving, borrowing, year, partner_id, funding_id, regDate = None):
        self.name = name,
        self.year_of_creation = year_of_creation
        self.member_female = member_female
        self.member_male = member_male
        self.sector_id = sector_id
        self.sg_status = sg_status
        self.saving = saving
        self.borrowing = borrowing
        self.year = year
        self.partner_id = partner_id
        self.funding_id = funding_id

        if regDate is None:
            self.regDate = datetime.utcnow()


class Ngo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(60))
    telephone = db.Column(db.String(30))
    website = db.Column(db.String(60))
    category = db.Column(db.Integer) # Int NGO 1 : Local NGO : 0
    picture = db.Column(db.String(100))
    address = db.Column(db.String(200))
    sg = db.relationship('SavingGroup', backref='ngo', lazy='dynamic')
    user = db.relationship('User', backref='ngo', lazy='dynamic')

    def __init__(self, name, email, telephone, website, category, picture, address):
        self.name = name
        self.email = email
        self.telephone = telephone
        self.website = website
        self.category = category
        self.picture = picture
        self.address = address


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(175))
    saved = db.Column(db.String(175))
    filename = db.Column(db.String(150))
    regDate = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    size = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, original, saved, filename, status, user_id, size, regDate=None):
        self.original = original
        self.saved = saved
        self.filename = filename
        self.status = status
        self.size = size
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
    finscope_district = db.relationship('Finscope', backref='district', lazy='dynamic')

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

    sector_bank = db.relationship('Bank', backref='sector', lazy='dynamic')
    sector_mfi = db.relationship('Mfi', backref='mfi', lazy='dynamic')
    sector_usacco = db.relationship('UmurengeSacco', backref='umurenge_sacco', lazy='dynamic')
    sector_nusacoo = db.relationship('NonUmurengeSacco', backref='non_umurenge_sacco', lazy='dynamic')
    sector_population = db.relationship('Population', backref='sector', lazy='dynamic')
    sg = db.relation('SavingGroup', backref='sector', lazy='dynamic')

    def __init__(self, id, name, code, district_code, district_id):
        self.id = id
        self.name = name
        self.code = code
        self.district_code = district_code
        self.district_id = district_id


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))

    def __init__(self, count, name, year, sector_id):
        self.count = count
        self.name = name
        self.year = year
        self.sector_id = sector_id


class Mfi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    name = db.Column(db.String(250))
    year = db.Column(db.Integer)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))

    def __init__(self, count, name, year, sector_id):
        self.count = count
        self.name = name
        self.year = year
        self.sector_id = sector_id


class UmurengeSacco(db.Model):
    __tablename__ = 'umurenge_sacco'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    name = db.Column(db.String(150))
    year = db.Column(db.Integer)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))

    def __init__(self, count, name, year, sector_id):
        self.count = count
        self.name = name
        self.year = year
        self.sector_id = sector_id


class NonUmurengeSacco(db.Model):
    __tablename__ = 'non_umurenge_sacco'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    name = db.Column(db.String(150))
    year = db.Column(db.Integer)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))

    def __init__(self, count, name, year, sector_id):
        self.count = count
        self.name = name
        self.year = year
        self.sector_id = sector_id


class BankAgent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    year = db.Column(db.Integer)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))

    def __init__(self, count, year, district_id):
        self.count = count
        self.year = year
        self.district_id = district_id


class TelcoAgent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    year = db.Column(db.Integer)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))

    def __init__(self, count, year, district_id):
        self.count = count
        self.year = year
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


class Finscope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    banked = db.Column(db.Integer)
    other_formal = db.Column(db.Integer)
    other_informal = db.Column(db.Integer)
    excluded = db.Column(db.Integer)
    year = db.Column(db.Integer)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))

    def __init__(self, banked, other_formal, other_informal, excluded, year, district_id):
        self.banked = banked
        self.other_formal = other_formal
        self.other_informal = other_informal
        self.excluded = excluded
        self.year = year
        self.district_id = district_id










