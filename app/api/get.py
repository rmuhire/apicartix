from app import *
from app.model.models import *
from app.model.schema import *
import datetime
from flask import jsonify

@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found, Please check ur route well.'

@app.route('/getsavinggroup')
def get_svg():
    svgs=SavingGroup.query.all()
    result=sgs_schema.dump(svgs)
    return jsonify({'Saving groups':result.data})


@app.route('/getsavingggroup/<name>')
def get_svgname(name):
    svg = SavingGroup.query.filter_by(name=name).first()
    if svg :
        result=sg_schema.dump(svg)
        return jsonify({'Message':'1','Saving Group':result.data})
    else:
        return jsonify({'Message':'0'})
