from app import *
from app.model.models import *
from sqlalchemy import text


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
        supervised_sql = text('select count(sg_status), funding_id from saving_group '
                              'WHERE sg_status = :val GROUP BY funding_id')
        result = db.engine.execute(supervised_sql, val='Supervised')
        supervised = []
        for row in result:
            data = [row[0], row[1]]
            supervised.append(data)

        # Graduated Query
        graduated_sql = text('select count(sg_status), funding_id from saving_group '
                              'WHERE sg_status = :val GROUP BY funding_id')
        result = db.engine.execute(graduated_sql, val='Graduated')
        graduated = []
        for row in result:
            data = [row[0], row[1]]
            graduated.append(data)

        return [supervised,graduated]


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
