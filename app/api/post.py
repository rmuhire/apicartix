from app.model.models import *
from app.model.schema import *
from flask import jsonify,request
import datetime


@app.route('/savinggroup/',methods=['POST'])
def svg():
    json_data=request.get_json()
    if not json_data:
        return jsonify({'Message':'No data provided'})
    data,errors=sg_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    #try:
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
    return jsonify({'Message':'1','Saving group':result.data})

    #except:
        #return jsonify({'Message':'0'})
