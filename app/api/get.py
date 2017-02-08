from app import *
from app.model.models import *
from app.model.schema import *
from flask import jsonify, send_from_directory
from kenessa import Province, District
from app.template.email import Email
import json
from app.controller.saving_year import generate_year
from app.controller.list_partner import litPartnerNgo
from sqlalchemy import and_




@app.route('/api/v1/users')
def users():
    user = User.query.all()
    if user:
        result = users_schema.dump(user)
        return jsonify({'users':result.data})
    else:
        return jsonify({'message':'0'})


@app.route('/api/v1/user/<int:id>')
def user(id):
    user = User.query.get(id)

    if user:
        result = user_schema.dump(user)
        return jsonify({'user':result.data})
    else:
        return jsonify({'message':'0'})


@app.route('/api/v1/user_role/<id>')
def user_role(id):
    user = User.query.get(id)
    if user.user_role:
        return jsonify({'status': True})
    return jsonify({'status': False})


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
def amount():
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
def ngos():
    ngo = Ngo.query.all()
    result = ngos_schema.dump(ngo).data
    return jsonify({'NGOs':result})


@app.route('/api/v1/ngo/<id>')
def ngo(id):
    ngo = Ngo.query.get(id)
    if ngo:
        result = ngo_schema.dump(ngo)
        return jsonify({'ngo':result.data})

    else:
        return jsonify({'Message':'0'})


@app.route('/api/v1/int_ngo/')
def int_ngo():
    ngo = Ngo.query.filter_by(category=1)
    if ngo:
        result = ngos_schema.dump(ngo)
        return jsonify(result.data)


@app.route('/api/v1/int_ngo/partner/<id>')
def intNgoPartner(id):
    ngo = Sgs.query.with_entities(Sgs.partner_id, Sgs.funding_id).filter(Sgs.funding_id.in_(id))
    if ngo:
        result = sgs_schemas.dump(ngo).data
        data = litPartnerNgo(result)

        partner = Ngo.query.filter(Ngo.id.in_(data))
        if partner:
            partner_ngo = ngos_schema.dump(partner).data
            return jsonify(partner_ngo, data)


@app.route('/api/v1/ngo_status/<id>')
def ngo_status(id):
    ngo = Ngo.query.get(id)
    try:
        if ngo.category:
            return jsonify({'status': True})
        return jsonify({'status': False})
    except AttributeError:
        return jsonify({'status': 'error'})



@app.route('/api/v1/province/<id>')
def province(id):
    province = json.loads(Province(id).province())
    return jsonify({'province':province})


@app.route('/api/v1/province/district/<id>')
def district(id):
    district = json.loads(Province(id).district())
    return jsonify(district)


@app.route("/api/v1/recover/<email>")
def recover(email):

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'result': False})

    status = Email(user.names, user.username, user.email).resetlink()

    return jsonify({'result': status})


@app.route('/api/v1/check/key/<email>/<key>')
def reset_password(email, key):
    user = User.query.filter(User.update_key == key).first()
    if user is None:
        return jsonify({'result' : False})

    return jsonify({'result' : True})


@app.route('/api/v1/save/<path:filename>', methods=['GET','POST'])
def read_saved(filename):
    uploads = '/home/www/cartix/uploads/save/'
    return send_from_directory(directory=uploads, filename=filename)


from kenessa import Province, District


@app.route('/api/v1/kenessa/province/province/<value>')
def provinceKen(value):
    province = Province(value).province()
    return jsonify(province)


@app.route('/api/v1/kenessa/province/district/<value>')
def districtKen(value):
    district = Province(value).district()
    return jsonify(district)


@app.route('/api/v1/kenessa/province/sector/<value>')
def sectorKen(value):
    sector = Province(value).sector()
    return jsonify(sector)


@app.route('/api/v1/kenessa/district/district/<value>')
def district_districtKen(value):
    district = District(value).district()
    return jsonify(district)


@app.route('/api/v1/kenessa/district/sector/<value>')
def district_sectorKen(value):
    sector = District(value).sector()
    return jsonify(sector)


@app.route('/api/v1/saving_year/')
def saving_year():
    year = generate_year()
    return jsonify(year)


# script updating rows on amount table

@app.route('/api/v1/rows/amount/')
def row_amount():
    amount = Amount.query.all()
    if amount:
        result = amounts_schema.dump(amount)

        for item in result.data:
            uniq_id = ''.join([str(item['year']), str(item['sg_id'])])
            queryAmount = Amount.query.get(item['id'])
            queryAmount.uniq_id = uniq_id
            db.session.commit()

        return jsonify('1')



@app.route('/api/v1/files')
def get_files():
    files = Files.query.all()
    if files:
        result = files_schema.dump(files).data
        return jsonify(result)


@app.route('/api/v1/files/user/<id>')
def get_user_file(id):
    files = Files.query.filter_by(user_id=id)
    if files:
        result = files_schema.dump(files).data
        return jsonify(result)


