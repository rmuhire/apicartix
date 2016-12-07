from app.model.models import *
from app.model.schema import *

def user_to_ngo(json_data):
    output={'user_ngo':[]}
    cat=""
    p = json_data['ngo_id']
    n = Ngo.query.get(p)

    if int(n.category) == 1:
        cat="funding"
    elif int(n.category) == 0:
        cat="partner"

    output['user_ngo'].append({'user_id':json_data['id'],'username':json_data['username'],'ngo_id':n.id,'ngo_name':n.name,'ngo_email':n.email,'ngo_telephone':n.telephone,'ngo_website':n.website,'ngo_category':cat,'picture':n.picture,'address':n.address})

    return output
