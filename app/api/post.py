from app.model.models import *
from app.model.schema import *
from flask import jsonify,request, session
from app.controller.exellentodb import Excellentodb, Financialdb, FinancialChecker
from app.controller.exellentodb import Excellento
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from app.controller.getusername import get_username
from werkzeug import secure_filename
from app.template.email import Email, help
import os
from app.controller.uniqid import uniqid
import json
from app.controller.location import Kendb, KenQuerydb
from app.controller.viewdata import DownloadExcel


bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['ALLOWED_EXTENSIONS'] = set(['xlsx','xls','csv','png'])


@app.route('/api/v1/params/', methods=['POST'])
def new_params():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    upload = json_data['upload']
    user_id = json_data['user_id']
    signup = json_data['signup']

    try:
        params = Params(
            upload=upload,
            signup=signup,
            regDate=None,
            user_id=user_id
        )
        db.session.add(params)
        db.session.commit()

        last_params = Params.query.get(params.id)
        result = param_schema.dump(last_params).data
        return jsonify(result)

    except IntegrityError:
        return jsonify(False)


@app.route('/api/v1/exellento',methods=['POST'])
def excellento():
    data = Excellentodb('faking_it_1.xlsx').toexcel()
    return jsonify({'data':data})


@app.route('/api/v1/visualize', methods=['POST'])
def visualize():
    data = Excellento('all.xlsx').json()
    return jsonify({'data':data})


@app.route('/api/v1/user/', methods=['POST'])
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
            update_key=None,
            upload=1,
            signup=1,
            ngo_id=data['ngo_id']
        )

        db.session.add(user)
        db.session.commit()

        last_user = user_schema.dump(User.query.get(user.id)).data
        Email(user.names, user.username, user.email).account()
        return jsonify({'result':True})

    except IntegrityError:
        return jsonify({'result': False})


@app.route('/api/v1/help/message/', methods=['POST'])
def help_message():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    name = json_data['names']
    email = json_data['email']
    title = json_data['title']
    message = json_data['message']
    username = json_data['username']

    sent_mail = help(name, email, title, message);
    return jsonify(sent_mail)


@app.route('/api/v1/ngo/', methods=['POST'])
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

        return jsonify({'result': ngo.id})

    except IntegrityError:
        db.session().rollback()
        ngo = Ngo.query.filter_by(name=data['name'].upper()).first()
        return jsonify({'result': ngo.id})


@app.route("/api/v1/login/", methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message':'no valid input provided'}), 400
    data, errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    username, password = data['username'], data['password']

    user = User.query.filter((User.username == username) | (User.email == username)).first()
    try:
        pw_hash = bcrypt.check_password_hash(user.password, password)
        if pw_hash:
            session['logged_in'] = True
            return jsonify({'result': user.id, 'ngo_id':user.ngo_id})
        else:
            status = False
            return jsonify({'result': status})
    except AttributeError:
        status = False
        return jsonify({'result': status})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/api/upload/', methods=['POST','GET'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        tmp_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(tmp_filename)

        file_name,file_extension = os.path.splitext(tmp_filename)

        re_filename = uniqid()+file_extension


        destination = "/Users/muhireremy/cartix/uploads/user/"+re_filename
        #destination = "/home/www/cartix/uploads/user/"+re_filename
        os.rename(tmp_filename, destination)

        status, data = Excellentodb(destination).toexcel()

        if status:
            return jsonify({'status':status,'json':data,'originalpath':destination, 'filename':filename})
        else:
            return jsonify({'status':status, 'savepath':data, 'originalpath':destination, 'filename':filename})

    else:
        return jsonify({'status':2})


@app.route('/api/v1/file/save/', methods=['POST'])
def file_save():

    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'no valid input provided'}), 400

    data, errors = file_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    size = os.path.getsize(data['original'])

    try:
        files = Files(
            original=data['original'],
            saved=data['saved'],
            filename=data['filename'],
            regDate=None,
            status=0,
            size=size,
            user_id=data['user_id']
        )

        db.session.add(files)
        db.session.commit()

        last_file = file_schema.dump(Files.query.get(files.id)).data
        return jsonify({'auth': 1, 'file': last_file})

    except IntegrityError:
        pass


@app.route('/api/v1/file/user/', methods=['POST'])
def file_user():

    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'no valid input provided'}), 400

    data, errors = file_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    size = os.path.getsize(data['original'])

    try:
        files = Files(
            original=data['original'],
            saved=data['saved'],
            filename=data['filename'],
            regDate=None,
            status=1,
            size=size,
            user_id=data['user_id']
        )

        db.session.add(files)
        db.session.commit()

        to_db = Excellentodb(data['original']).todb()

        last_file = file_schema.dump(Files.query.get(files.id)).data
        return jsonify({'auth': 1, 'file': last_file,'todb':to_db})

    except IntegrityError:
        return jsonify({'auth':0})


""" Runing Test """

@app.route('/api/v1/email/<names>/<username>/<email>')
def send_email(names, username, email):
    Email(names, username, email).account()
    return jsonify({'email':'send'})


@app.route('/api/v1/reset/<names>/<username>/<email>')
def send_email_reset(names, username, email):
    Email(names, username, email).resetlink()
    return jsonify({'email':'send'})


@app.route('/api/v1/success/<names>/<username>/<email>')
def send_email_success(names, username, email):
    Email(names, username, email).resetsuccess()
    return jsonify({'email':'send'})


@app.route('/api/v1/province/')
def province_json():
    json_province = json.loads(open('json/province.json').read())
    result = Kendb(json_province).province()

    return jsonify({'status':result})

@app.route('/api/v1/district/')
def district_json():
    json_district = json.loads(open('json/district.json').read())
    result = Kendb(json_district).district()

    return jsonify({'status': result})


@app.route('/api/v1/sector/')
def sector_json():
    json_sector = json.loads(open('json/sector.json').read())
    result = Kendb(json_sector).sector()

    return jsonify({'status': result})


@app.route('/api/v1/pro')
def pro():
    data = KenQuerydb('1').province()
    return jsonify(data)


@app.route('/api/v1/dis')
def dis():
    data = KenQuerydb('nyarugenge').district()
    return jsonify(data)


@app.route('/api/v1/sec')
def sec():
    data = KenQuerydb('remera').sector()
    return jsonify(data)


@app.route("/api/v1/data/finance")
def data_finance():
    folder = "/Users/muhireremy/cartix/test/data_2016/"
    bank = Excellento(folder + "bank_2016.xls").json_data()
    mfi = Excellento(folder + "mfi_2016.xls").json_data()
    usacco = Excellento(folder + "usacco_2016.xls").json_data()
    nusacco = Excellento(folder + "nusacco_2016.xls").json_data()
    bank_agent = Excellento(folder + "bank_agent_2016.xlsx").json_data()
    telco_agent = Excellento(folder + "telco_agent_2016.xls").json_data()

    """data_bank = FinancialChecker(bank,'bank_2016').excel()
    data_mfi = FinancialChecker(mfi,'mfi_2016').excel()
    data_usacco = FinancialChecker(usacco,'usacco_2016').excel()
    data_nusacco = FinancialChecker(nusacco,'nusacco_2016').excel()
    data_bank_agent = FinancialChecker(bank_agent,'bank_agent_2016').excel()
    data_telco_agent = FinancialChecker(telco_agent,'telco_agent_2016').excel()"""

    data_bank = Financialdb(bank).bank()
    data_mfi = Financialdb(mfi).mfi()
    data_usacco = Financialdb(usacco).usacco()
    data_nusacco = Financialdb(nusacco).nusacco()
    data_bank_agent = Financialdb(bank_agent).bank_agent()
    data_telco_agent = Financialdb(telco_agent).telco_agent()

    return jsonify({
        "bank":data_bank,
        "mfi":data_mfi,
        "usacco":data_usacco,
        "nusacco":data_nusacco,
        "bank agent":data_bank_agent,
        "telco_agent":data_telco_agent
    })

    return jsonify({"status": data_bank_agent})


@app.route("/api/v1/data/finscope")
def data_finscope():
    """folder = "/Users/muhireremy/cartix/test/data/"
    fin_2012 = Excellento(folder + "newF2012.xlsx").json_data()
    fin_2015 = Excellento(folder + "newF2015.xlsx").json_data()

    data_2012 =Financialdb(fin_2012).finscope()
    data_2015 = Financialdb(fin_2015).finscope()

    return jsonify({
        "2012":data_2012,
        "2015":data_2015
    })"""

    return jsonify({
        "status":"already added"
    })


@app.route('/api/v1/data/download/', methods=['POST'])
def download_excel():
    json_data = request.get_json()
    query = json_data['query']
    year = json_data['year']
    query = DownloadExcel(query, year).download()
    return jsonify(query)


