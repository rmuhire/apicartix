from app import *
from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
from flask import jsonify,request
import datetime
from app.controller.exellentodb import Excellentodb
from app.controller.exellentodb import Excellento
from app.controller.get_username import *
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
import platform
from app.controller.geoloc import *
from datetime import datetime

mail=Mail(app)

@app.route('/api/v1/exellento',methods=['POST'])
def excellento():
    data = Excellentodb('faking_it.xlsx').toexcel()
    return jsonify({'data':data})


@app.route('/api/v1/visualize', methods=['POST'])
def visualize():
    data = Excellento('all.xlsx').json()
    return jsonify({'data':data})
#==================================================INDIVIDUAL POST==========================================================

@app.route('/api/v1/savinggroup/',methods=['POST'])
def svg():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=sg_schema.load(json_data)
    if errors:
        return jsonify(errors), 422


@app.route('/api/v1/amount/',methods=['POST'])
def amount():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors= amount_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    try:
        amt = Amount(
            saving = data['saving'],
            borrowing = data['borrowing'],
            year = data['year'],
            sg_id = data['sg_id']
            )
        db.session.add(amt)
        db.session.commit()
        result = amount_schema.dump(Amount.query.get(amt.id))
        return jsonify({'Amount':result.data})

    except:
        return jsonify({'Message':'0'})


@app.route('/api/v1/user/', methods=['POST'])
def add_user():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    username = get_username(data['email'])
    pwd_hash = bcrypt.generate_password_hash(data['password'])

    try:
        user = User(
            names=data['names'],
            username=username,
            email=data['email'],
            phone=None,
            user_role=None,
            regDate=None,
            password=pwd_hash,
            gender=None,
            ngo_id=data['ngo_id']
        )

        db.session.add(user)
        db.session.commit()

        last_user = user_schema.dump(User.query.get(user.id)).data
        loc=geoloc()
        date=datetime.utcnow()
        plat=platform.system()
        msg = Message('Hello', sender = 'no-reply@cartix.io', recipients = [data['email']])
        msg.html ="""<html lang="en"> <head> <title>Cartix-mail</title> </head> <body style="background-color:#F5F5F5"> <div style="margin: auto;width: 60%; padding: 10px;" class="container"> <!-- First Container --> <div style="background-color: #560034;" > <div class="cartix-logo"> <img style="display:block;margin:0 auto;padding-bottom: 50px;padding-top:50px;margin-top:60px;" src="http://cartix.io/assets/img/mail/cartix_logo.png" height="120" > </div> </div> <div style="padding-top:40px;height:250px;background-color:white"> <h2 style="text-align:left;color:#616161;";>Hi {username}, Your Cartix Account Was Created Succesfully.</h1> <div style="margin-top:12px" class="content"> <p style="text-align:justify;color:#212121;font-size:60%;">Date:<span style="text-align:right;font-weight:bold;" class=""> {date}</span></p> <p style="text-align:justify;color:#212121;font-size:60%;">Operating System:<span style="text-align:right;font-weight:bold;" class=""> {loc}</span></p> <p style="text-align:justify;color:#212121;font-size:60%;">Aproximate location:<span style="text-align:right;font-weight:bold;" class=""> {loc}</span></p> </div> <div style="" class="btn-box"> </div> </div> </div> </div> </div> </body></html>""".format(username=username,date=date,plat=plat,loc=loc)

        mail.send(msg)
        return jsonify({'auth':1, 'user':last_user})

    except IntegrityError:
        return jsonify({'auth': 0, 'user': 'Already added.'})


@app.route('/api/v1/ngo/', methods=['POST'])
def add_ngo():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message':'No input data provided'}), 400

    data, errors = ngo_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        ngo = Ngo(
            name=data['name'].upper(),
            email=data['email'],
            telephone=None,
            website=None,
            category=data['category'],
            picture=None,
            address=None
        )

        db.session.add(ngo)
        db.session.commit()

        last_ngo = ngo_schema.dump(Ngo.query.get(ngo.id)).data
        return jsonify({'auth':1, 'ngo':last_ngo})

    except IntegrityError:
        db.session().rollback()
        ngo = Ngo.query.filter_by(name=data['name'].upper()).first()
        ngo_id = ngo.id
        return jsonify({'auth': 0, 'ngo': ngo_id})


@app.route('/api/v1/pafu/',methods=['POST'])
def prf():
     json_data=request.get_json()
     if not json_data:
         return jsonify({'Message':'No data provided'})
     data,errors=partner_schema.load(json_data)
     if errors:
         return jsonify(errors), 422
     sgss= Sgs(
        partner_id=data['partner_id'],
        funding_id=data['funding_id']
       )
     db.session.add(sgss)
     db.session.commit()
     result=sgfp_schema.dump(Sgs.query.get(sgss.id))

#===========================================LOG IN==================================

@app.route('/api/v1/login/',methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Message':'No input data provided'}), 400
    data,errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    username,password = data['username'],data['password']

    user = User.query.filter((User.username==username) | (User.email==username)).first()

    try:
        pw_hash = bcrypt.check_password_hash(user.password, password)
        if pw_hash:
            result = user_schema.dump(User.query.get(user.id))
            return jsonify({'auth': 1, 'user': result.data})
        else:
            return jsonify({'auth': 0})
    except AttributeError:
        return jsonify({'auth':2})
