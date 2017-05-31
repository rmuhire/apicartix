from app.model.models import *
from flask_bcrypt import Bcrypt
from flask import jsonify,request
from app.template.email import Email
from sqlalchemy.exc import IntegrityError

bcrypt = Bcrypt(app)


@app.route('/api/v1/change/password', methods=["PUT"])
def change_password():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'result':False})

    email = json_data['email']
    pw_hash = bcrypt.generate_password_hash(json_data['password'])

    user = User.query.filter_by(email = email).first()

    user.password = pw_hash
    user.update_key = None
    db.session.commit()

    status = Email(user.names, user.username, user.email).resetsuccess()

    return jsonify({'result':status})


@app.route('/api/v1/users/<int:id>', methods=['PUT'])
def edit_users(id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'result':False})

    names = json_data['names']
    email = json_data['email']

    try:
        user = User.query.get(id)
        user.email = email
        user.names = names
        db.session.commit()
        return jsonify(True)
    except IntegrityError:
        return jsonify(False)


@app.route('/api/v1/users/check_password/<int:id>', methods=['PUT'])
def check_password(id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'result': False})

    password = json_data['password']
    try:
        user = User.query.get(id)
        pw_hash = bcrypt.check_password_hash(user.password, password)
        if pw_hash:
            return jsonify(True)
        else:
            return jsonify(False)

    except IntegrityError:
        return jsonify(False)


@app.route('/api/v1/change/password/<int:id>', methods=["PUT"])
def change_password_id(id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'result':False})

    pw_hash = bcrypt.generate_password_hash(json_data['password'])

    user = User.query.get(id)

    user.password = pw_hash
    user.update_key = None
    db.session.commit()

    status = Email(user.names, user.username, user.email).resetsuccess()

    return jsonify(status)

