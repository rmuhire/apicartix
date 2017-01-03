from app import *
from app.model.models import *
from app.model.schema import *
from flask import jsonify, send_from_directory
from kenessa import Province
from app.template.email import Email
import json




@flask_app.route('/api/v1/users')
def users():
    user = User.query.all()
    if user:
        result = users_schema.dump(user)
        return jsonify({'users':result.data})
    else:
        return jsonify({'message':'0'})


@flask_app.route('/api/v1/user/<int:id>')
def user(id):
    user = User.query.get(id)

    if user:
        result = user_schema.dump(user)
        return jsonify({'user':result.data})
    else:
        return jsonify({'message':'0'})


@flask_app.route('/api/v1/sg')
def sg():
    sg = SavingGroup.query.all()
    result = sgs_schema.dump(sg)
    return jsonify({'Saving groups':result.data})


@flask_app.route('/api/v1/sg/<name>')
def sg_name(name):
    sg = SavingGroup.query.filter_by(name=name).first()
    if sg:
        result=sg_schema.dump(sg)
        return jsonify({'Saving Group':result.data})
    else:
        return jsonify({'Message':'0'})


@flask_app.route('/api/v1/amount')
def amount():
    amount = Amount.query.all()
    result = amounts_schema.dump(amount).data
    return jsonify({'Amounts':result})


@flask_app.route('/api/v1/amount/<int:id>')
def amount_sg(id):
    amount = Amount.query.filter_by(sg_id=id).first()
    if amount:
        result = amount_schema.dump(amount)
        return jsonify({'SG-Amount':result.data})
    else:
        return jsonify({'Message':'0'})


@flask_app.route('/api/v1/ngos')
def ngos():
    ngo = Ngo.query.all()
    result = ngos_schema.dump(ngo).data
    return jsonify({'NGOs':result})


@flask_app.route('/api/v1/ngo/<id>')
def ngo(id):
    ngo = Ngo.query.get(id)
    if ngo:
        result = ngo_schema.dump(ngo)
        return jsonify({'ngo':result.data})

    else:
        return jsonify({'Message':'0'})


@flask_app.route('/api/v1/province/<id>')
def province(id):
    province = json.loads(Province(id).province())
    return jsonify({'province':province})


@flask_app.route('/api/v1/province/district/<id>')
def district(id):
    district = json.loads(Province(id).district())
    return jsonify(district)


@flask_app.route("/api/v1/recover/<email>")
def recover(email):

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'result': False})

    status = Email(user.names, user.username, user.email).resetlink()

    return jsonify({'result': status})


@flask_app.route('/api/v1/check/key/<email>/<key>')
def reset_password(email, key):
    user = User.query.filter(User.update_key == key).first()
    if user is None:
        return jsonify({'result' : False})

    return jsonify({'result' : True})


@flask_app.route('/api/v1/save/<path:filename>', methods=['GET', 'POST'])
def read_saved(filename):
    uploads = '/home/www/cartix/uploads/save/'
    return send_from_directory(directory=uploads, filename=filename)