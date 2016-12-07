from app import *
from app.model.models import *
from app.model.schema import *
from flask import request
from datetime import date
from datetime import time
from flask import jsonify
from app.controller.cont import *
from flask_mail import Mail, Message
from random import randint
from app.controller.user_to_ngo import *

mail=Mail(app)

@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found, Please check ur route well.'


@app.route('/api/v1/users')
def users_():
    user = User.query.all()
    if user:
        result = users_schema.dump(user)
        return jsonify({'users':result.data})
    else:
        return jsonify({'message':'0'})

@app.route('/api/v1/user/<int:uid>')
def user_(uid):
    user = User.query.get(uid)

    if user:
        result = user_schema.dump(user)
        return jsonify({'user':result.data})

    else:
        return jsonify({'message':'0'})



@app.route('/api/v1/sg')
def sg():
    sg = SavingGroup.query.all()
    result = sgs_schema.dump(sg)
    return jsonify({'saving groups':result.data})


@app.route('/api/v1/sg/<name>')
def sg_name(name):
    sg = SavingGroup.query.filter_by(name=name).first()
    if sg:
        result=sg_schema.dump(sg)
        return jsonify({'saving Group':result.data})
    else:
        return jsonify({'message':'0'})



@app.route('/api/v1/amount')
def amountss():
    amount = Amount.query.all()
    result = amounts_schema.dump(amount).data
    return jsonify({'amounts':result})

@app.route('/api/v1/amount/<int:id>')
def amount_sg(id):
    amount = Amount.query.filter_by(sg_id=id).first()
    if amount:
        result = amount_schema.dump(amount)
        return jsonify({'sg-amount':result.data})
    else:
        return jsonify({'message':'0'})

@app.route('/api/v1/ngos')
def get_fuaa():
    funs = Ngo.query.all()
    result = ngos_schema.dump(funs).data
    return jsonify({'ngos':result})

@app.route('/api/v1/ngo/<int:nid>')
def get_fun(nid):
    ng = Ngo.query.get(nid)
    if ng:
        result = ngo_schema.dump(ng)
        return jsonify({'ngo':result.data})

    else:
        return jsonify({'message':'0'})


@app.route('/api/v1/getFuPas')
def get_fupas():
    fupa = Sgs.query.all()
    result = sgfps_schema.dump(fupa)
    return jsonify({'funding-partner':result.data})

@app.route('/api/v1/getFuPa/<int:id>')
def getfup(id):
    fupa = Sgs.query.filter_by(id=id)
    if fupa:
        result = sgfp_schema.dump(fupa)
        return jsonify({'funding-partner':result.data})
    else:
        return jsonify({'message':'0'})


#======================================== PASSWORD RECOVERY ==========================


@app.route("/api/v1/recover/<email>")
def recover(email):
    df = User.query.filter_by(email=email).first()
    if df is None:
        return jsonify({'Message':"0"})
    else:
        x=randint(100, 9999)
        msg = Message('Hello', sender = 'getlunchex@gmail.com', recipients = [df.email])
        msg.body = "your code is {}".format(x)
        mail.send(msg)
        dd=x

        try:
            sa=Cover.query.filter_by(user_id=df.id).first()
            if sa:
                db.session.delete(sa)
                fj=Cover(user_id = df.id,code = dd)
                db.session.add(fj)
                db.session.commit()
                return jsonify({"message":"1"})
            else:
                fj=Cover(user_id = df.id,code = dd)
                db.session.add(fj)
                db.session.commit()
                return jsonify({"message":"1"})

        except:
            return jsonify({'message':'Error'})


@app.route("/api/v1/rec/<code>/<pas>")
def rec(code,pas):
    ll=Cover.query.filter_by(code = code ).order_by(Cover.user_id.desc()).first()
    if ll is None:
        return jsonify({'message':'0'})
    else:
        ld=User.query.filter_by(id=ll.user_id).first()
        if ld is None:
            return jsonify({'message':'0'})
        else:
            json_data=user_schema.dump(ld).data
            pas = changePass(json_data,pas);

            ld.password=pas
            db.session.commit()

            return jsonify({"message":'1'})


#============================================ USER TO NGO ==============================================

@app.route('/api/v1/usertongo/<int:uid>')
def us_id(uid):
    user = User.query.get(uid)
    if user is None:
        return jsonify({'message':'0'})
    else:
        json_data=user_schema.dump(user).data
        ngo = user_to_ngo(json_data);
        return jsonify(ngo)
