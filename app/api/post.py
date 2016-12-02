from app import *
from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
<<<<<<< HEAD
import datetime
from app.controller.excellentodb import Excellentodb
from app.controller.excellentodb import Excellento
=======
from app.controller.exellentodb import Excellentodb
from app.controller.exellentodb import Excellento
>>>>>>> adbe3c21f962ebc11d982a0db95ded910abbc530

#==================================================INDIVIDUAL POST==========================================================

<<<<<<< HEAD
@app.route('/api/v1/savinggroup/',methods=['POST'])
def svg():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=sg_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
=======
@app.route('/api/v1/exellento',methods=['POST'])
def excellento():
    data = Excellentodb('fake_data.xlsx').toexcel()
    return jsonify({'data':data})
>>>>>>> adbe3c21f962ebc11d982a0db95ded910abbc530


@app.route('/api/v1/visualize', methods=['POST'])
def visualize():
    data = Excellento('all.xlsx').json()
    return jsonify({'data':data})

<<<<<<< HEAD
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

@app.route('/api/v1/ngo/',methods=['POST'])
def fundg():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=ngo_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    pw_hash = bcrypt.generate_password_hash(data['password'])

    #try:
    ngo = Ngo(
            name= data['name'],
            email= data['email'],
            username = data['username'],
            category = data['category'],
            website = "",
            picture= "",
            telephone = "",
            address = data['address'],
            cp_name = data['cp_name'],
            cp_email = data['cp_email'],
            cp_telephone = data['cp_telephone'],
            password = pw_hash
            )
    db.session.add(ngo)
    db.session.commit()
    result = ngo_schema.dump(Ngo.query.get(ngo.id))
    return jsonify({'NGO':result.data})
    #except:
    #    return jsonify({'Message':'0'})

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


@app.route('/api/v1/excellento',methods=['POST'])
def excellento():
    data = Excellentodb('faking_it.xlsx').todb()
    return jsonify({'data':data})


@app.route('/api/v1/visualize', methods=['POST'])
def visualize():
    data = Excellento('sg_datas.xlsx').json()
    return jsonify({'data':data})


#===========================================LOG IN==================================

@app.route('/api/v1/login/',methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Message':'No input data provided'}), 400
    data,errors = ngo_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    name,password = data['name'],data['password']

    ngo = Ngo.query.filter(Ngo.name==name).first()

    try:
        pw_hash = bcrypt.check_password_hash(ngo.password, password)
        if pw_hash:
            result = ngo_schema.dump(Ngo.query.get(ngo.id))
            return jsonify({'auth': 1, 'ngo': result.data})
        else:
            return jsonify({'auth': 0})
    except AttributeError:
        return jsonify({'auth':2})


    #ngo = Ngo.query.filter_by(name=name,password=password).first()
    #if ngo is None:
    #    return jsonify({'Message':'0'})
    #else:
    #    res = ngo_schema.dump(Ngo.query.get(ngo.id))
    #    return jsonify({'Message':'1','NGO':res.data})
=======
>>>>>>> adbe3c21f962ebc11d982a0db95ded910abbc530
