from app.model.models import *
from sqlalchemy import and_


def check_sgs(local_ngo_id, intl_ngo_id, sg_id):
    sgs = Sgs.query.filter(and_(Sgs.funding_id == intl_ngo_id, Sgs.partner_id == local_ngo_id, Sgs.sg_id == sg_id)).first()
    if sgs:
        import pdb; pdb.set_trace()
        return False
    return True