from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
from app.controller.exellentodb import Excellentodb


@app.route('/api/v1/exellento',methods=['POST'])
def excellento():
    data = Excellentodb('all.xlsx').todb()


    return jsonify({'data':data})


