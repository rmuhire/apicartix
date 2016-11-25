from app import *
from app.model.models import *
from app.model.schema import *
from flask import request
#import datetime
from datetime import date
#from datetime import datetime, timedelta
from datetime import time
#from datetime import timedelta
from flask import jsonify

@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found, Please check ur route well.'

@app.route('/getsavinggroup')
def get_svg():
    svgs=SavingGroup.query.all()
    result=sgs_schema.dump(svgs)
    return jsonify({'Saving groups':result.data})


@app.route('/getsavinggroup/<name>')
def get_svgname(name):
    svg = SavingGroup.query.filter_by(name=name).first()
    if svg :
        result=sg_schema.dump(svg)
        return jsonify({'Saving Group':result.data})
    else:
        return jsonify({'Message':'0'})


@app.route('/getAmount')
def get_am():
    ams = Amount.query.all()
    result = amounts_schema.dump(ams).data
    return jsonify({'Amounts':result})

@app.route('/getAmount/<int:sgid>')
def get_ams(sgid):
    ams = Amount.query.filter_by(sg_id=sgid).first()
    if ams:
        result = amount_schema.dump(ams)
        return jsonify({'SG-Amount':result.data})
    else:
        return jsonify({'Message':'0'})

@app.route('/getfundings')
def get_fu():
    funs = Funding.query.all()
    result = fundings_schema.dump(funs).data
    return jsonify({'Funding NGOs':result})

@app.route('/getfunding/<name>')
def get_fun(name):
    fun = Funding.query.filter_by(name=name)
    if fun:
        result = funding_schema.dump(fun)
        return jsonify({'Funding NGO':result.data})

    else:
        return jsonify({'Message':'0'})

@app.route('/getpartners')
def get_pa():
    parts = Partner.query.all()
    result = partners_schema.dump(parts).data
    return jsonify({'Partner NGOs':result})

@app.route('/getpartner/<name>')
def get_pas(name):
    fun = Funding.query.filter_by(name=name)
    if fun:
        result = funding_schema.dump(fun)
        return jsonify({'Partner NGO':result.data})

    else:
        return jsonify({'Message':'0'})

@app.route('/getFuPas')
def get_fupas():
    fupa = Sgs.query.all()
    result = sgfps_schema.dump(fupa)
    return jsonify({'Funding-Partner':result.data})

@app.route('/getFuPa/<int:id>')
def getfup(id):
    fupa = Sgs.query.filter_by(id=id)
    if fupa:
        result = sgfp_schema.dump(fupa)
        return jsonify({'Funding-Partner':result.data})
    else:
        return jsonify({'Message':'0'})

#===========================================LOG IN==================================

@app.route('/funding/login/',methods=['POST'])
def f_login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Message':'No input data provided'}), 400
    data,errors=funding_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    name,password = data['name'],data['password']
    funding_ngo=Funding.query.filter_by(name=name,password=password).first()
    if funding_ngo is None:
        return jsonify({'Message':'0'})
    else:
        res=funding_schema.dump(Funding.query.get(funding_ngo.id))
        return jsonify({'Message':'1','Funding_NGO':res.data})


@app.route('/partner/login/',methods=['POST'])
def p_login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Message':'No input data provided'}), 400
    data,errors=partner_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    name,password = data['name'],data['password']
    partner_ngo=Partner.query.filter_by(name=name,password=password).first()
    if partner_ngo is None:
        return jsonify({'Message':'0'})
    else:
        res=partner_schema.dump(Partner.query.get(partner_ngo.id))
        return jsonify({'Message':'1','Partner_NGO':res.data})
