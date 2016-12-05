from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
from app.controller.exellentodb import Excellentodb
from app.controller.exellentodb import Excellento
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from app.controller.getusername import get_username

bcrypt = Bcrypt(app)


@app.route('/api/v1/exellento',methods=['POST'])
def excellento():
    data = Excellentodb('faking_it_1.xlsx').toexcel()
    return jsonify({'data':data})


@app.route('/api/v1/visualize', methods=['POST'])
def visualize():
    data = Excellento('all.xlsx').json()
    return jsonify({'data':data})


@app.route('/api/v1/user', methods=['POST'])
def add_user():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    username = get_username(data['email'])
    pwd_hash = bcrypt.generate_password_hash(data['password'])

    try:
        user = User(
            names=data['names'],
            username=username,
            email=data['email'],
            phone=None,
            user_role=None,
            regDate=None,
            password=pwd_hash,
            gender=None,
            ngo_id=data['ngo_id']
        )

        db.session.add(user)
        db.session.commit()

        last_user = user_schema.dump(User.query.get(user.id)).data
        return jsonify({'auth':1, 'user':last_user})

    except IntegrityError:
        return jsonify({'auth': 0, 'user': 'Already added.'})


@app.route('/api/v1/ngo', methods=['POST'])
def add_ngo():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message':'No input data provided'}), 400

    data, errors = ngo_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        ngo = Ngo(
            name=data['name'].upper(),
            email=None,
            telephone=None,
            website=None,
            category=data['category'],
            picture=None,
            address=None
        )

        db.session.add(ngo)
        db.session.commit()

        last_ngo = ngo_schema.dump(Ngo.query.get(ngo.id)).data
        return jsonify({'auth':1, 'ngo':last_ngo})

    except IntegrityError:
        db.session().rollback()
        ngo = Ngo.query.filter_by(name=data['name'].upper()).first()
        ngo_id = ngo.id
        return jsonify({'auth': 0, 'ngo': ngo_id})





