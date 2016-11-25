from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
import datetime
from app.controllers.Excellento import exc_json


@app.route('/submission/'.methods=['POST'])
def subm():
    json_data=Excellento('path')
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=sg_schema.load(json_data)
    dat,errors=amount_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    try:
        svgs=SavingGroup(
            name=data['name'],
            year=data['year'],
            member_female=data['member_female'],
            member_male=data['member_male'],
            sector_id=data['sector_id'],
            regDate=datetime.datetime.utcnow()
            )
        amt = Amount(
            saving = dat['saving'],
            borrowing = dat['borrowing'],
            year = dat['year'],
            sg_id = dat['sg_id']
            )
        sg = Sgs(

        )

        db.session.add(amt)
        db.session.add(svgs)
        db.session.commit()

        res = amount_schema.dump(Amount.query.get(amt.id))
        result=sg_schema.dump(SavingGroup.query.get(svgs.id))
        return jsonify({'Saving group':result.data,'Amount':res.data})

    except:
        return jsonify({'Message':'0'})





























#==================================================INDIVIDUAL POST==========================================================

@app.route('/savinggroup/',methods=['POST'])
def svg():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=sg_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    try:
        svgs=SavingGroup(
            name=data['name'],
            year=data['year'],
            member_female=data['member_female'],
            member_male=data['member_male'],
            sector_id=data['sector_id'],
            regDate=datetime.datetime.utcnow()
            )
        db.session.add(svgs)
        db.session.commit()
        result=sg_schema.dump(SavingGroup.query.get(svgs.id))
        return jsonify({'Saving group':result.data})

    except:
        return jsonify({'Message':'0'})

@app.route('/amount/',methods=['POST'])
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

@app.route('/funding/',methods=['POST'])
def fundg():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=funding_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    try:
        fund = Funding(
            name=data['name'],
            email=data['email'],
            username=data['username'],
            cp_name=data['cp_name'],
            cp_email=data['cp_email'],
            cp_telephone=data['cp_telephone'],
            password=data['password']
            )
        db.session.add(fund)
        db.session.commit()
        result = funding_schema.dump(Funding.query.get(fund.id))
        return jsonify({'Funding':result.data})
    except:
        return jsonify({'Message':'0'})

@app.route('/partner/',methods=['POST'])
def partn():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=partner_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    try:
        fund = Partner(
            name = data['name'],
            email = data['email'],
            username = data['username'],
            cp_name = data['cp_name'],
            cp_email = data['cp_email'],
            cp_telephone = data['cp_telephone'],
            password = data['password']
            )
        db.session.add(fund)
        db.session.commit()
        result = partner_schema.dump(Partner.query.get(fund.id))
        return jsonify({'Partner':result.data})
    except:
        return jsonify({'Message':'0'})

@app.route('/pafu/',methods=['POST'])
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
