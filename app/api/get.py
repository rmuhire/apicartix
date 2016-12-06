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

mail=Mail(app)

@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found, Please check ur route well.'


@app.route('/api/v1/users')
def users_():
    user = User.query.all()
    result = users_schema.dump(user)
    return jsonify({'Users':result.data})

@app.route('/api/v1/user/<name>')
def user_(name):
    user = User.query.filter((User.username== name) | (User.email== name)).first()

    if user:
        result = user_schema.dump(user)
        return jsonify({'User':result.data})

    else:
        return jsonify({'Message:0'})



@app.route('/api/v1/sg')
def sg():
    sg = SavingGroup.query.all()
    result = sgs_schema.dump(sg)
    return jsonify({'Saving groups':result.data})


@app.route('/api/v1/sg/<name>')
def sg_name(name):
    sg = SavingGroup.query.filter_by(name=name).first()
    if sg:
        result=sg_schema.dump(sg)
        return jsonify({'Saving Group':result.data})
    else:
        return jsonify({'Message':'0'})



@app.route('/api/v1/amount')
def amountss():
    amount = Amount.query.all()
    result = amounts_schema.dump(amount).data
    return jsonify({'Amounts':result})

@app.route('/api/v1/amount/<int:id>')
def amount_sg(id):
    amount = Amount.query.filter_by(sg_id=id).first()
    if amount:
        result = amount_schema.dump(amount)
        return jsonify({'SG-Amount':result.data})
    else:
        return jsonify({'Message':'0'})

@app.route('/api/v1/ngos')
def get_fuaa():
    funs = Ngo.query.all()
    result = ngos_schema.dump(funs).data
    return jsonify({'NGOs':result})

@app.route('/api/v1/ngo/<name>')
def get_fun(name):
    ng = Ngo.query.filter_by(name=name).first()
    if ng:
        result = ngo_schema.dump(ng)
        return jsonify({'NGO':result.data})

    else:
        return jsonify({'Message':'0'})


@app.route('/api/v1/getFuPas')
def get_fupas():
    fupa = Sgs.query.all()
    result = sgfps_schema.dump(fupa)
    return jsonify({'Funding-Partner':result.data})

@app.route('/api/v1/getFuPa/<int:id>')
def getfup(id):
    fupa = Sgs.query.filter_by(id=id)
    if fupa:
        result = sgfp_schema.dump(fupa)
        return jsonify({'Funding-Partner':result.data})
    else:
        return jsonify({'Message':'0'})


#======================================== PASSWORD RECOVERY ==========================


@app.route("/api/v1/recover/<email>")
def recover(email):
    df=User.query.filter_by(email=email).first()
    if df is None:
        return jsonify({'Message':"0"})
    else:
        x=randint(100, 9999)
        msg = Message('Hello', sender = 'getlunchex@gmail.com', recipients = [df.email])
        msg.body = "your code is {}".format(x)
        mail.send(msg)
        dd=x

        try:
            sa=Cover.query.filter_by(ngo_id=df.id)
            if sa is None:
                db.session.delete(sa)
                fj=Cover(ngo_id = df.id,code = dd)
                db.session.add(fj)
                db.session.commit()
                return jsonify({"Message":"1"})
            else:
                fj=Cover(ngo_id = df.id,code = dd)
                db.session.add(fj)
                db.session.commit()
                return jsonify({"Message":"1"})

        except:
            return jsonify({'Message':'Error'})


@app.route("/api/v1/rec/<code>/<pas>")
def rec(code,pas):
    ll=Cover.query.filter_by(code = code ).order_by(Cover.ngo_id.desc()).first()
    if ll is None:
        return jsonify({'Message':'0'})
    else:
        ld=Ngo.query.filter_by(id=ll.ngo_id).first()
        if ld is None:
            return jsonify({'Message':'0'})
        else:
            json_data=ngo_schema.dump(ld).data
            pas = changePass(json_data,pas);

            ld.password=pas
            db.session.commit()

            return jsonify({"Message":'1'})

'''@app.route('/api/v1/ngos')
def ngos():
    ngo = Ngo.query.all()
    result = ngos_schema.dump(ngo).data
    return jsonify({'NGOs':result})

@app.route('/api/v1/ngo/<name>')
def ngo(name):
    ngo = Ngo.query.filter_by(name=name).first()
    if ngo:
        result = ngo_schema.dump(ngo)
        return jsonify({'NGO':result.data})

    else:
        return jsonify({'Message':'0'})'''
