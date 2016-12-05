from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
from app.controller.exellentodb import Excellentodb
from app.controller.exellentodb import Excellento
from sqlalchemy.exc import IntegrityError


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
    pass


@app.route('/api/v1/ngo', methods=['POST'])
def add_ngo():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message':'No input data provided'}), 400

    data, errors = ngo_schema(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        ngo = Ngo(
            name=data['name'],
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
        return jsonify({'auth': 0, 'ngo': 'Ngo has been added'})





