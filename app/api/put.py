from app.model.models import *
from flask_bcrypt import Bcrypt
from flask import jsonify,request
from app.template.email import Email

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




