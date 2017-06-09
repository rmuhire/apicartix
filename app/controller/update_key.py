from app.model.models import *


def update_key(email, key):

    user = User.query.filter_by(email=email).first()
    user.update_key = key
    db.session.commit()
    return True





