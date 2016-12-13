from app import *
from app.model.models import *
from app.model.schema import *
from flask import request
from datetime import date
from datetime import time
from flask import jsonify,render_template
from app.controller.cont import *
from flask_mail import Mail, Message
from random import randint
from app.controller.user_to_ngo import *
from datetime import datetime
import platform
from app.controller.geoloc import *
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
    amount = Amount.query.filter_bby(sg_id=id).first()
    if amount:
        result = amount_schema.dump(amount)
        return jsonify({'sg-amount':result.data})
    else:
        return jsonify({'message':'0'})

@app.route('/api/v1/ngos')
def get_fuaas():
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
        msg = Message('Hello', sender = 'noreply@cartix.io', recipients = [df.email])
        msg.html ="""<body style="background-color:#7F4646  ;margin:50px;text-align:center;padding:40px;font-size:150%;font-weight:bold"><br><span style="color:white;font-size:250%;text-align:center">CARTIX</span><br><br><br><span style="color:white">HELLO, Your Cartix Recovery Password Is:</span><br><br><span style="text-align:center;color:white;padding:3cm;font-style:oblique;font-size:150%">{code}</span></body>""".format(code=x)
        #msg.html="""<!DOCTYPE html><html lang="en"> <head> <title>Cartix-mail</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet"> <link rel="shortcut icon" href="img/cartix-favicon.png" type="image/x-icon"> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> <link rel="stylesheet" href="http://cartix.io/assets/css/style_mail.css"> </head> <body> <!-- First Container --> <div class="container bg-1 text-center"> <div class="box-container"> <div class="row"> <div class="col-md-6"> <img src="http://cartix.io/assets/img/mail/cartix_logo.png" class="cartix-icon"> </div> <div class="col-md-6"> <img src="http://cartix.io/assets/img/mail/mail-icon.png" class=" mail-icon"> </div> </div> </div> </div> <div class="container bg-2 text-center"> <div class="box-container-2"> <h1 class="text-left">Your Password Recovery Code Is:</h1> <p class="text-left">{code}</p> </div> <div class="btn-box"> <div class="row"> <div class="col-md-3 col-md-offset-3"></div> <div class="col-md-3 col-md-offset-3"> <button type="button" class="btn btn-success btn-mail">Confirm</button> </div> </div> </div> <div class="mail-footer"> <img src="http://cartix.io/assets/img/mail/mail_footer.png" class="img-responsive"> </div> </div> </div> </body></html""".format(code=x)
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
            loc=geoloc()
            date=datetime.utcnow()
            plat=platform.system()
            msg = Message('Hello', sender = 'noreply@cartix.io', recipients = [ld.email])
            msg.html ="""<body style="background-color:#7F4646  ;margin:50px;text-align:center;padding:40px;font-size:150%;font-weight:bold"><br><span style="color:white;font-size:250%;text-align:center">CARTIX</span><br><br><br><span style="color:white">HELLO, Your Cartix Password Was Recovered Successfully</span><br><br><span style="text-align:center;color:white;padding:3cm;font-style:oblique;font-size:50%">this happened at :{date}</span><br><span style="text-align:center;color:white;padding:3cm;font-style:oblique;font-size:50%">operting system :{plat}</span><br><span style="text-align:center;color:white;padding:3cm;font-style:oblique;font-size:50%">Location : {loc}</span></body>""".format(date=date,plat=plat,loc=loc)
            mail.send(msg)
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
