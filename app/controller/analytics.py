from app.model.models import *
from sqlalchemy import text
from saving_year import creation_year


class MapAnalytics:
    def __init__(self):
        pass

    def provinceAnalytics(self):
        sql_province = text('select count(saving_group.name)'
                            ', sum(saving_group.member_female) '
                            ', sum(saving_group.member_male)'
                            ', sum(saving_group.borrowing)'
                            ', sum(saving_group.saving)'
                            ', province.name '
                            'from saving_group, sector, district, province '
                            'where sector.id = saving_group.sector_id AND '
                            'district.id = sector.district_id AND '
                            'province.id = district.province_id '
                            'group by province.name')
        result = db.engine.execute(sql_province)
        province = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5]]
            province.append(data)
        return province

    def districtAnalytics(self):
        sql_district = text('select count(saving_group.name)'
                            ', sum(saving_group.member_female) '
                            ', sum(saving_group.member_male)'
                            ', sum(saving_group.borrowing)'
                            ', sum(saving_group.saving)'
                            ', district.name '
                            'from saving_group, sector, district '
                            'where sector.id = saving_group.sector_id AND '
                            'saving_group.borrowing != :x AND '
                            'saving_group.saving != :x AND '
                            'district.id = sector.district_id '
                            'group by district.id')

        result = db.engine.execute(sql_district, x=-1)
        district = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5]]
            district.append(data)
        return district

    def sectorAnalytics(self):
        sql_district = text('select count(saving_group.name)'
                            ', sum(saving_group.member_female) '
                            ', sum(saving_group.member_male)'
                            ', sum(saving_group.borrowing)'
                            ', sum(saving_group.saving)'
                            ', sector.name'
                            ', sector.district_id '
                            'from saving_group, sector '
                            'where sector.id = saving_group.sector_id '
                            'AND saving_group.borrowing != :x AND '
                            'saving_group.saving != :x '
                            'group by sector.id')
        result = db.engine.execute(sql_district, x=-1)
        sector = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5], returnDistrict(row[6])]
            sector.append(data)
        return sector

    def json(self):
        province = MapAnalytics().provinceAnalytics()
        district = MapAnalytics().districtAnalytics()
        sector = MapAnalytics().sectorAnalytics()

        # Province

        provinces = []
        for i in range(len(province)):
            data = {}
            value = province[i]
            data['Province'] = returnProvince(value[5])
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            data['borrowing'] = value[3]
            data['saving'] = value[4]
            provinces.append(data)

        # District

        districts = []
        for i in range(len(district)):
            data = {}
            value = district[i]
            data['District'] = value[5].title()
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            data['borrowing'] = value[3]
            data['saving'] = value[4]
            districts.append(data)

        # Sector

        sectors = []
        for i in range(len(sector)):
            data = {}
            value = sector[i]
            data['District'] = value[6].title()
            data['Sector'] = value[5].title()
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            data['borrowing'] = value[3]
            data['saving'] = value[4]
            sectors.append(data)

        return [provinces, districts, sectors]


class ChartAnalytics:
    def __init__(self):
        pass

    # Membership per gender
    def membership(self):
        membership_sql = text('select sum(member_female)'
                              ', sum(member_male) from saving_group, sector'
                              ' where sector.id = saving_group.sector_id')
        result = db.engine.execute(membership_sql)

        val = []
        labels = ['Male Members', 'Female Members']
        for row in result:
            val = [row[0], row[1]]

        data = []
        item = {}
        item['values'] = val
        item['labels'] = labels
        item['type'] = 'pie'

        data.append(item)

        return data

    # SGS_status per Intl NGOs
    def sg_status(self):

        # Supervised query
        supervised_sql = text('select count(sg_status), partner_id from saving_group '
                              'WHERE sg_status = :val GROUP BY partner_id')
        result = db.engine.execute(supervised_sql, val='Supervised')
        supervised = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            supervised.append(data)

        # Graduated Query
        graduated_sql = text('select count(sg_status), partner_id from saving_group '
                              'WHERE sg_status = :val GROUP BY partner_id')
        result = db.engine.execute(graduated_sql, val='Graduated')
        graduated = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            graduated.append(data)

        supervised, graduated = renderStatusArray(supervised, graduated)

        # Supervised x y classification
        x = []
        y = []
        for item in supervised:
            x.append(item[1])
            y.append(item[0])

        # Json Supervised
        json_sup = {}
        json_sup['x'] = x
        json_sup['y'] = y
        json_sup['name'] = 'Supervised'
        json_sup['type'] = 'bar'

        # Graduated x y classification
        x = []
        y = []
        for item in graduated:
            x.append(item[1])
            y.append(item[0])

        json_grad = {}
        json_grad['x'] = x
        json_grad['y'] = y
        json_grad['name'] = 'Graduated'
        json_grad['type'] = 'bar'

        return [json_sup, json_grad]

    # SG Savings and Loans per Intl NGOs
    def savings_loans(self):

        # Savings query
        saving_sql = text('select sum(saving), partner_id from saving_group '
                          'where saving <> -1 '
                          'GROUP by partner_id')
        result = db.engine.execute(saving_sql)

        saving = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            saving.append(data)

        # Loans query
        loan_sql = text('select sum(borrowing), partner_id from saving_group '
                          'where saving <> -1 '
                          'GROUP by partner_id')
        result = db.engine.execute(loan_sql)
        loan = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            loan.append(data)

        # sort array
        saving = sortArray(saving)
        loan = sortArray(loan)

        #return [saving, loan]

        # Saving x y classification
        x = []
        y = []
        for item in saving:
            x.append(item[1])
            y.append(item[0])

        json_saving = dict()
        json_saving['x'] = x
        json_saving['y'] = y
        json_saving['name'] = 'Savings'
        json_saving['type'] = 'bar'

        # Loan x y classification
        x = []
        y = []
        for item in loan:
            x.append(item[1])
            y.append(item[0])

        json_loan = dict()
        json_loan['x'] = x
        json_loan['y'] = y
        json_loan['name'] = 'Loans'
        json_loan['type'] = 'bar'

        return [json_saving, json_loan]

    # Saving Group creation year
    def creation(self):
        years = creation_year()
        data = []
        for year in years:
            yearlist = list()
            year_sql = text('select count(id), partner_id from saving_group '
                            'where year_of_creation = :year '
                            'GROUP BY partner_id')
            result = db.engine.execute(year_sql, year=year)
            for row in result:
                val = [row[0], getNgoName(row[1])]
                yearlist.append(val)

            data.append(sortArray(yearlist))

        trace = []
        for i in range(len(data)):
            x = []
            y = []
            json = dict()
            for item in data[i]:
                x.append(item[1])
                y.append(item[0])
            json['x'] = x
            json['y'] = y
            json['name'] = years[i]
            json['type'] = 'bar'
            trace.append(json)

        return trace

    def savingPerIntNgo(self):
        sql = text('select count(saving_group.id),'
                   ' ngo.id,'
                   ' ngo.name'
                   ' from saving_group,'
                   ' ngo where saving_group.partner_id = ngo.id'
                   ' AND saving_group.year = 2014'
                   ' group by ngo.id')

        result = db.engine.execute(sql)
        values = list()
        labels = list()
        for row in result:
            values.append(row[0])
            labels.append(row[2])

        json = dict()
        json['values'] = values
        json['labels'] = labels
        json['type'] = 'pie'

        return [json]

    def localPerIntNgo(self):
        sql = text('select distinct(funding_id)'
                    ' from saving_group'
                    ' where year = 2014')
        result = db.engine.execute(sql)
        data = list()
        for row in result:
            funding_id = row[0]
            x = list()
            y = list()
            sql = text('select distinct(partner_id),'
                       ' count(id)'
                       ' from saving_group'
                       ' where funding_id = :funding_id'
                       ' group by partner_id')
            re = db.engine.execute(sql, funding_id=funding_id)
            for item in re:
                x.append(getNgoName(item[0]))
                y.append(item[1])
            json = dict()
            json['x'] = x
            json['y'] = y
            json['name'] = getNgoName(funding_id)
            json['type'] = 'bar'
            data.append(json)
        return data

    def sgFinancialInstitution(self):
        sql_sg = text('select count(saving_group.id),'
                      ' province.name'
                      ' from saving_group,'
                      ' sector, district,'
                      ' province where sector.id = saving_group.sector_id'
                      ' AND district.id = sector.district_id'
                      ' AND province.id = district.province_id'
                      ' group by province.name'
                      ' order by province.name')
        result = db.engine.execute(sql_sg)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        # Bank Data
        sql_banks = text('select sum(bank.count),'
                         ' province.name'
                         ' from bank,'
                         ' sector,'
                         ' district,'
                         ' province'
                         ' where sector.id = bank.sector_id'
                         ' AND district.id = sector.district_id'
                         ' AND province.id = district.province_id'
                         ' group by province.name order'
                         ' by province.name')
        result = db.engine.execute(sql_banks)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_bank = dict()
        json_bank['x'] = x
        json_bank['y'] = y
        json_bank['name'] = 'Banks'
        json_bank['type'] = 'bar'


        # mfi
        sql_mfi = text('select sum(mfi.count),'
                       ' province.name'
                       ' from mfi, sector, district, province '
                       'where sector.id = mfi.sector_id AND'
                       ' district.id = sector.district_id AND'
                       ' province.id = district.province_id group by'
                       ' province.name order by province.name')
        result = db.engine.execute(sql_mfi)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_mfi = dict()
        json_mfi['x'] = x
        json_mfi['y'] = y
        json_mfi['name'] = 'MFIs'
        json_mfi['type'] = 'bar'

        # umurenge sacco

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' province.name'
                          ' from umurenge_sacco, sector, district, province'
                          ' where sector.id = umurenge_sacco.sector_id AND'
                          ' district.id = sector.district_id AND'
                          ' province.id = district.province_id'
                          ' group by province.name'
                          ' order by province.name')
        result = db.engine.execute(sql_usacco)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_usacco = dict()
        json_usacco['x'] = x
        json_usacco['y'] = y
        json_usacco['name'] = 'Umurenge Sacco'
        json_usacco['type'] = 'bar'

        # Non - Umurenge Sacco

        sql_nusacco = text('select sum(non_umurenge_sacco.count),'
                           ' province.name'
                           ' from non_umurenge_sacco, sector, district, province'
                           ' where sector.id = non_umurenge_sacco.sector_id'
                           ' AND district.id = sector.district_id '
                           'AND province.id = district.province_id '
                           'group by province.name '
                           'order by province.name')
        result = db.engine.execute(sql_nusacco)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_nusacco = dict()
        json_nusacco['x'] = x
        json_nusacco['y'] = y
        json_nusacco['name'] = 'Non-Umurenge Sacco'
        json_nusacco['type'] = 'bar'

        return [json_sg, json_bank, json_mfi, json_usacco, json_nusacco]

    def sgTelcoAgent(self):
        # telco agent
        sql_telco = text('select sum(telco_agent.count),'
                         ' province.name'
                         ' from telco_agent, province, district'
                         ' where telco_agent.district_id = district.id '
                         'and district.province_id = province.id '
                         'group by province.name '
                         'order by province.name')
        result = db.engine.execute(sql_telco)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_telco = dict()
        json_telco['x'] = x
        json_telco['y'] = y
        json_telco['name'] = 'Telco Agents'
        json_telco['type'] = 'bar'

        # bank agent
        sql_bank = text('select sum(bank_agent.count),'
                         ' province.name'
                         ' from bank_agent, province, district'
                         ' where bank_agent.district_id = district.id '
                         'and district.province_id = province.id '
                         'group by province.name '
                         'order by province.name')
        result = db.engine.execute(sql_bank)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_bank = dict()
        json_bank['x'] = x
        json_bank['y'] = y
        json_bank['name'] = 'Bank Agents'
        json_bank['type'] = 'bar'

        # sg

        sql_sg = text('select count(saving_group.id),'
                      ' province.name'
                      ' from saving_group,'
                      ' sector, district,'
                      ' province where sector.id = saving_group.sector_id'
                      ' AND district.id = sector.district_id'
                      ' AND province.id = district.province_id'
                      ' group by province.name'
                      ' order by province.name')
        result = db.engine.execute(sql_sg)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        return [json_sg, json_telco, json_bank]


class NumberAnalytics:
    def __init__(self, year):
        self.year = year

    def numbers(self):
        sql_number =  text('select count(id),'
                           ' sum(member_female),'
                           ' sum(member_male),'
                           ' sum(saving),'
                           ' sum(borrowing)'
                           ' from saving_group'
                           ' where year = :year')
        result = db.engine.execute(sql_number, year = self.year)
        if result:
            for row in result:
                if row[1] is None:
                    return [0,0,0,0]
                data = [row[0],row[1] + row[2], row[3], row[4]]
            return data


def returnProvince(name):
    val = ['kigali', 'north', 'south', 'west', 'east']
    data = ['Kigali City', 'Northern', 'Southern', 'Western', 'Eastern']

    for i in range(len(val)):
        if name == val[i]:
            return data[i]


def returnDistrict(id):
    district = text('select name from district where id = :id')
    result = db.engine.execute(district, id=id)

    for row in result:
        return row[0]


def renderStatusArray(supervised, graduated):
    i = 0
    for x in graduated:
        for y in supervised:
            if x[1] == y[1]:
                i = 1
            val = x[1]
        if i == 0:
            supervised.append([0, val])
        i = 0

    i = 0
    for x in supervised:
        for y in graduated:
            if x[1] == y[1]:
                i = 1
            val = x[1]
        if i == 0:
            graduated.append([0, val])
        i = 0

    return [sortArray(supervised),sortArray(graduated)]


def sortArray(list):
    sorted_array =  sorted(list, key=lambda x: x[1])
    return sorted_array


def getNgoName(id):
    ngo = text('select name from ngo where id = :id')
    result = db.engine.execute(ngo, id=id)
    for row in result:
        return row[0]



