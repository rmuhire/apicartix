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
import templates
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
        msg = Message('Hello', sender = 'no-reply@cartix.io', recipients = [df.email])
        msg.html="""<html lang="en"> <head> <title>Cartix-mail</title> </head> <body style="background-color:#F5F5F5"> <div style="margin: auto;width: 60%; padding: 10px;" class="container"> <!-- First Container --> <div style="background-color: #560034;" > <div class="cartix-logo"> <img style="display:block;margin:0 auto;padding-bottom: 50px;padding-top:50px;margin-top:60px;" src="http://cartix.io/assets/img/mail/cartix_logo.png" height="120" > <!-- <img style="margin-left: 100px;" src="img//mail-icon.png " height="250" class="mail-logo"> --> <!-- <img style="margin-left: 100px;" src="http://cartix.io/assets/img/mail/mail-icon.png " height="250" class="mail-logo"> --> </div> </div> <div style="padding-top:40px;height:210px;background-color:white"> <h3 style="text-align:center;color:#616161">Hi {username}, <br><span style="color:#616161">Your Cartix Password Recovery Code Is:</span></h3> <p style="text-align:center;color:#212121;font-size:150%;font-weight:bold">{code}</p> <div style="" class="btn-box"> <button style="margin-bottom:20px;display:block;margin:0 auto;background-color:#00C853;border:2px solid #00C853; border-radius:25px;color:white;height:30px;font-weight:bold;" type="button">Confirm</button> </div> <!-- <img src="img/footer_image.png" height="122" > --> <!-- <img src="http://cartix.io/assets/img/mail/mail_footer.png" height="122" > --> </div> </div> </div> </div> </body></html>""".format(username=df.username,code=x)
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
            msg = Message('Hello', sender = 'no-reply@cartix.io', recipients = [ld.email])
            msg.html ="""<html lang="en"> <head> <title>Cartix-mail</title> </head> <body style="background-color:#757575"> <img style="margin-left:290px;margin-top:20px;height:50px;" src="http://cartix.io/assets/img/mail/cartix_logo.png"> <div style="margin: auto;width: 60%; padding: 10px;" class="container"> <!-- First Container --> <div style="margin-top:0px;padding-bottom:25px;background-color:white;" > <p style="margin-left:12px;padding-top:35px;color:#424242">Hallo {username},</p> <p style="margin-left:12px;color:#424242">You've successfully changed your Cartix password.</p> <p style="margin-left:12px;color:#424242">For any inquiry e-mail us on info@cartix.io or call us on +250 785-489-992</p> <p style="margin-left:12px;color:#424242">Thank you for using Cartix!</p> <p style="margin-left:12px;color:#424242">Cartix Team</p> </div> <div style=";height:200px;background-color:#EEEEEE;"> <h3 style="margin-left:12px;padding-top:30px;text-align:left;color:#212121">when and where this happened</h3> <div style="" class="content"> <p style="margin-left:12px;text-align:justify;color:white;font-size:80%;color:#212121">Date:<span style="text-align:right;font-weight:bold;" class=""> {date}</span></p> <p style="margin-left:12px;text-align:justify;color:white;font-size:80%;color:#212121">Operating System:<span style="text-align:right;font-weight:bold;" class=""> {plat}</span></p> <p style="margin-left:12px;text-align:justify;color:white;font-size:80%;color:#212121">Aproximate location:<span style="text-align:right;font-weight:bold;" class=""> {loc}</span></p> </div> <div style="" class="btn-box"> </div> </div> </div> </div> </div> </body></html>""".format(username=ld.username,date=date,plat=plat,loc=loc)
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
