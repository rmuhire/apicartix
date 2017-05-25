from app import *
from app.model.models import *
from app.model.schema import *
from flask import jsonify, send_from_directory
from app.template.email import Email
import json
from app.controller.saving_year import generate_year
from app.controller.analytics import MapAnalytics, ChartAnalytics, NumberAnalytics, listNgo
from app.controller.convert_size import convert_array_file_size
from app.controller.location import KenQuerydbJson
from app.controller.viewdata import ViewData, ngoName, DownloadExcel
from sqlalchemy import text


@app.route('/api/v1/users')
def users():
    user = User.query.all()
    if user:
        result = users_schema.dump(user)
        return jsonify({'users':result.data})
    else:
        return jsonify({'message':'0'})


@app.route('/api/v1/user/<int:id>')
def user(id):
    user = User.query.get(id)

    if user:
        result = user_schema.dump(user)
        return jsonify({'user':result.data})
    else:
        return jsonify({'message':'0'})


@app.route('/api/v1/user_role/<id>')
def user_role(id):
    user = User.query.get(id)
    if user.user_role:
        return jsonify({'status': True})
    return jsonify({'status': False})


@app.route('/api/v1/sg')
def sg():
    sg = SavingGroup.query.all()
    result = sgs_schema.dump(sg)
    return jsonify({'Saving groups':result.data})


@app.route('/api/v1/sg/<name>')
def sg_name(name):
    sg = SavingGroup.query.filter_by(name=name).first()
    if sg:
        result=sg_schema.dump(sg)
        return jsonify({'Saving Group':result.data})
    else:
        return jsonify({'Message':'0'})



@app.route('/api/v1/ngos')
def ngos():
    ngo = Ngo.query.all()
    result = ngos_schema.dump(ngo).data
    return jsonify({'NGOs':result})


@app.route('/api/v1/ngo/<id>')
def ngo(id):
    ngo = Ngo.query.get(id)
    if ngo:
        result = ngo_schema.dump(ngo)
        return jsonify({'ngo':result.data})

    else:
        return jsonify({'Message':'0'})


@app.route('/api/v1/int_ngo/')
def int_ngo():
    data = listNgo()
    return jsonify(data)


@app.route('/api/v1/int_ngo/partner/<id>')
def intNgoPartner(id):
    query = text("select distinct(saving_group.funding_id)" \
            " from saving_group, ngo" \
            " where saving_group.partner_id = ngo.id" \
            " and saving_group.partner_id = :id")
    result = db.engine.execute(query, id=id)
    data = list()
    for row in result:
        x = dict()
        x['name'] = ngoName(row[0])
        x['id'] = row[0]
        data.append(x)
    return jsonify(data)


@app.route('/api/v1/ngo_status/<id>')
def ngo_status(id):
    ngo = Ngo.query.get(id)
    try:
        if ngo.category:
            return jsonify({'status': True})
        return jsonify({'status': False})
    except AttributeError:
        return jsonify({'status': 'error'})


@app.route('/api/v1/province/<id>')
def province(id):
    province = json.loads(Province(id).province())
    return jsonify({'province':province})


@app.route('/api/v1/province/district/<id>')
def district(id):
    district = json.loads(Province(id).district())
    return jsonify(district)


@app.route("/api/v1/recover/<email>")
def recover(email):

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'result': False})

    status = Email(user.names, user.username, user.email).resetlink()

    return jsonify({'result': status})


@app.route('/api/v1/check/key/<email>/<key>')
def reset_password(email, key):
    user = User.query.filter(User.update_key == key).first()
    if user is None:
        return jsonify({'result' : False})

    return jsonify({'result' : True})


@app.route('/api/v1/save/<path:filename>', methods=['GET','POST'])
def read_saved(filename):
    uploads = '/home/www/cartix/uploads/save/'
    return send_from_directory(directory=uploads, filename=filename)


from kenessa import Province, District


@app.route('/api/v1/kenessa/province/province/<value>')
def provinceKen(value):
    province = Province(value).province()
    return jsonify(province)


@app.route('/api/v1/kenessa/province/district/<value>')
def districtKen(value):
    district = Province(value).district()
    return jsonify(district)


@app.route('/api/v1/kenessa/province/sector/<value>')
def sectorKen(value):
    sector = Province(value).sector()
    return jsonify(sector)


@app.route('/api/v1/kenessa/district/district/<value>')
def district_districtKen(value):
    district = District(value).district()
    return jsonify(district)


@app.route('/api/v1/kenessa/district/sector/<value>')
def district_sectorKen(value):
    sector = District(value).sector()
    return jsonify(sector)


@app.route('/api/v1/saving_year/')
def saving_year():
    year = generate_year()
    return jsonify(year)


@app.route('/api/v1/files')
def get_files():
    files = Files.query.all().order_by(Files.regDate.desc())
    if files:
        result = convert_array_file_size(files_schema.dump(files).data)
        return jsonify(result)


@app.route('/api/v1/files/user/<id>')
def get_user_file(id):
    files = Files.query.filter_by(user_id=id).order_by(Files.regDate.desc())
    if files:
        result = convert_array_file_size(files_schema.dump(files).data)
        return jsonify(result)


@app.route('/api/v1/saving')
def saving_group():
    sg = db.session.query(db.func.count(SavingGroup.name),
                          db.func.sum(SavingGroup.member_female),
                          db.func.sum(SavingGroup.member_male),
                          db.func.sum(SavingGroup.borrowing),
                          db.func.sum(SavingGroup.saving),
                          SavingGroup.sector_id).\
        join(Sector, SavingGroup.sector_id == Sector.id).\
        filter(SavingGroup.sector_id == Sector.id).\
        group_by(SavingGroup.sector_id).all()
    return jsonify([i for i in sg])


@app.route('/api/v1/sqlsaving/<sg>/<year>')
def sql_saving(sg, year):
    province, district, sector = MapAnalytics(sg.split(","), year).json()
    #val = MapAnalytics(sg, year).json()
    #return jsonify(val.split(","))
    #query = MapAnalytics(sg.split(","), year).provinceAnalytics()
    #return jsonify(query)
    return jsonify({
        "Provinces": province,
        "Districts": district,
        "Sectors": sector
    })


@app.route('/api/v1/chartanalytics/<int:year>/<ngo>')
def chartanalytics(year, ngo):
    membership = ChartAnalytics(year, ngo).membership()
    status = ChartAnalytics(year, ngo).sg_status()
    amount = ChartAnalytics(year, ngo).savings_loans()
    sg = ChartAnalytics(year, ngo).savingPerIntNgo()
    localPerIntNgo = ChartAnalytics(year, ngo).localPerIntNgo()
    sgFinancial = ChartAnalytics(year, ngo).sgFinancialInstitution()
    sgAgent = ChartAnalytics(year, ngo).sgTelcoAgent()
    finscope = ChartAnalytics(year, ngo).finscope()
    finscope_sg_2012, finscope_sg_2015 = ChartAnalytics(year, ngo).finscope_sg()
    finscope_all_2012 = ChartAnalytics(year, ngo).finscope_all(2012)
    finscope_all_2015 = ChartAnalytics(year, ngo).finscope_all(2015)

    return jsonify({
        "membership": membership,
        "status": status,
        "amount": amount,
        "sg":sg,
        "sgNgos":localPerIntNgo,
        "sgFinancial": sgFinancial,
        "sgAgent": sgAgent,
        "finscope":finscope,
        "finscope_sg_2012":[finscope_sg_2012],
        "finscope_sg_2015":[finscope_sg_2015],
        "finscope_all_2012": finscope_all_2012,
        "finscope_all_2015": finscope_all_2015
    })


@app.route('/api/v1/analytics/creation/<int:year>/<ngo>')
def membership_chart(year, ngo):
    creation = ChartAnalytics(year, ngo).creation()

    return jsonify({
        "creation":creation
    })


@app.route('/api/v1/analytics/numbers/<int:year>')
def numbers(year):
    sg_count, membership, saving, borrowing = NumberAnalytics(year).numbers()
    return jsonify({
        "sg_count": sg_count,
        "membership": membership,
        "saving": saving,
        "borrowing": borrowing
    })


@app.route('/api/v1/chart/sg_intngo/<int:year>')
def sg_intNgo(year):
    finscope_all_2012 = ChartAnalytics(year).finscope_all(2012)
    finscope_all_2015 = ChartAnalytics(year).finscope_all(2015)
    return jsonify({
        'finscope_all_2012':finscope_all_2012,
        'finscope_all_2015':finscope_all_2015
    })


@app.route('/api/v1/data/district/<province>')
def data_district(province):
    district = KenQuerydbJson(province).district()
    return jsonify(district)


@app.route('/api/v1/data/sector/<district>')
def data_sector(district):
    sector = KenQuerydbJson(district).sector()
    return jsonify(sector)


@app.route('/api/v1/data/view/<province>/<district>/<sector>/<ngo>/<year>/<int:type>')
def view_data(province, district, sector, ngo, year, type):
    data = ViewData(province, district, sector, ngo, year, type).viewData()
    graduated = ViewData(province, district, sector, ngo, year, type).viewDataGraduated()
    supervided = ViewData(province, district, sector, ngo, year, type).viewDataSupervised()
    year_of_creation = ViewData(province, district, sector, ngo, year, type).viewDataYearOfCreation()
    query = ViewData(province, district, sector, ngo, year, type).queryDownload()
    if type == 2:
        funding_ngo = ViewData(province, district, sector, ngo, year, type).viewDataPartnerNgo()
    else:
        funding_ngo = ViewData(province, district, sector, ngo, year, type).viewDataFundingNgo()

    data_json = dict()
    data_json['saving_group'] = data[0]
    data_json['member_female'] = data[1]
    data_json['member_male'] = data[2]
    data_json['total_member'] = data[1] + data[2]
    data_json['funding_ngo'] = funding_ngo
    data_json['year_of_creation'] = year_of_creation
    data_json['supervised'] = supervided
    data_json['graduated'] = graduated
    data_json['saving'] = data[3]
    data_json['borrowing'] = data[4]
    data_json['query'] = query

    return jsonify(data_json)


