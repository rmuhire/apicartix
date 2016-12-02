from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
from app.controller.exellentodb import Excellentodb
from app.controller.exellentodb import Excellento


@app.route('/api/v1/exellento',methods=['POST'])
def excellento():
    data = Excellentodb('fake_data.xlsx').toexcel()
    return jsonify({'data':data})


@app.route('/api/v1/visualize', methods=['POST'])
def visualize():
    data = Excellento('all.xlsx').json()
    return jsonify({'data':data})

