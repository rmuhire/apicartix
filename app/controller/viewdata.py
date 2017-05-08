from app.model.models import *
from sqlalchemy import text


class ViewData:
    def __init__(self, province, district, sector, ngo, year, type):
        self.provinces = province.split(",")
        self.districts = district.split(",")
        self.sectors = sector.split(",")
        self.ngos = ngo.split(",")
        self.year = int(year)
        self.type = type

    def viewData(self):
        query = "select count(saving_group.id)," \
                " sum(saving_group.member_female)," \
                " sum(saving_group.member_male)," \
                " sum(saving_group.saving)," \
                " sum(saving_group.borrowing)" \
                " from saving_group," \
                " province," \
                " district," \
                " sector," \
                " ngo" \
                " where saving_group.sector_id =sector.id" \
                " and sector.district_id = district.id" \
                " and district.province_id = province.id" \
                " and saving_group.partner_id = ngo.id" \
                " and saving_group.year = :year"

        if self.provinces != ['null']:
            mini_query = miniQueryProvince(self.provinces)
            query += " and "+ mini_query

        if self.districts != ['null']:
            mini_query = miniQueryDistrict(self.districts)
            query += " and " + mini_query

        if self.sectors != ['null']:
            mini_query = miniQuerySector(self.sectors)
            query += " and " + mini_query

        if self.ngos != ['null']:
            if self.type == 0:
                mini_query = miniQueryNgo(self.ngos)
            else:
                mini_query = miniQueryLocalNgo(self.ngos)
            query += " and " + mini_query

        sql_query = text(query)
        result = db.engine.execute(sql_query, year=self.year)

        for row in result:
            data = [
                    convertNonType(row[0]),
                    convertNonType(row[1]),
                    convertNonType(row[2]),
                    convertNonType(row[3]),
                    convertNonType(row[4])
            ]

        return data

    def viewDataGraduated(self):
        query = "select count(sg_status)" \
                " from saving_group," \
                " province," \
                " district," \
                " sector," \
                " ngo" \
                " where saving_group.sector_id =sector.id" \
                " and sector.district_id = district.id" \
                " and district.province_id = province.id" \
                " and saving_group.partner_id = ngo.id" \
                " and sg_status = :val" \
                " and saving_group.year = :year"

        if self.provinces != ['null']:
            mini_query = miniQueryProvince(self.provinces)
            query += " and "+ mini_query

        if self.districts != ['null']:
            mini_query = miniQueryDistrict(self.districts)
            query += " and " + mini_query

        if self.sectors != ['null']:
            mini_query = miniQuerySector(self.sectors)
            query += " and " + mini_query

        if self.ngos != ['null']:
            if self.type == 0:
                mini_query = miniQueryNgo(self.ngos)
            else:
                mini_query = miniQueryLocalNgo(self.ngos)
            query += " and " + mini_query

        sql_query = text(query)
        result = db.engine.execute(sql_query, val='Graduated', year=self.year)
        for row in result:
            data = row[0]

        return data

    def viewDataSupervised(self):
        query = "select count(sg_status)" \
                " from saving_group," \
                " province," \
                " district," \
                " sector," \
                " ngo" \
                " where saving_group.sector_id =sector.id" \
                " and sector.district_id = district.id" \
                " and district.province_id = province.id" \
                " and saving_group.partner_id = ngo.id" \
                " and sg_status = :val" \
                " and saving_group.year = :year"

        if self.provinces != ['null']:
            mini_query = miniQueryProvince(self.provinces)
            query += " and " + mini_query

        if self.districts != ['null']:
            mini_query = miniQueryDistrict(self.districts)
            query += " and " + mini_query

        if self.sectors != ['null']:
            mini_query = miniQuerySector(self.sectors)
            query += " and " + mini_query

        if self.ngos != ['null']:
            if self.type == 0:
                mini_query = miniQueryNgo(self.ngos)
            else:
                mini_query = miniQueryLocalNgo(self.ngos)
            query += " and " + mini_query

        sql_query = text(query)
        result = db.engine.execute(sql_query, val='Supervised', year=self.year)
        for row in result:
            data = row[0]

        return data

    def viewDataYearOfCreation(self):
        query = "select distinct(year_of_creation)" \
                " from saving_group," \
                " province," \
                " district," \
                " sector," \
                " ngo" \
                " where saving_group.sector_id =sector.id" \
                " and sector.district_id = district.id" \
                " and district.province_id = province.id" \
                " and saving_group.partner_id = ngo.id" \
                " and saving_group.year_of_creation <= :year"

        if self.provinces != ['null']:
            mini_query = miniQueryProvince(self.provinces)
            query += " and " + mini_query

        if self.districts != ['null']:
            mini_query = miniQueryDistrict(self.districts)
            query += " and " + mini_query

        if self.sectors != ['null']:
            mini_query = miniQuerySector(self.sectors)
            query += " and " + mini_query

        if self.ngos != ['null']:
            if self.type == 0:
                mini_query = miniQueryNgo(self.ngos)
            else:
                mini_query = miniQueryLocalNgo(self.ngos)
            query += " and " + mini_query

        sql_query = text(query)
        result = db.engine.execute(sql_query, year=self.year)
        data = list()
        for row in result:
            data.append(row[0])

        return data

    def viewDataFundingNgo(self):
        query = "select distinct(saving_group.funding_id)" \
                " from saving_group," \
                " province," \
                " district," \
                " sector," \
                " ngo" \
                " where saving_group.sector_id =sector.id" \
                " and sector.district_id = district.id" \
                " and district.province_id = province.id" \
                " and saving_group.partner_id = ngo.id" \
                " and saving_group.year = :year"

        if self.provinces != ['null']:
            mini_query = miniQueryProvince(self.provinces)
            query += " and " + mini_query

        if self.districts != ['null']:
            mini_query = miniQueryDistrict(self.districts)
            query += " and " + mini_query

        if self.sectors != ['null']:
            mini_query = miniQuerySector(self.sectors)
            query += " and " + mini_query

        if self.ngos != ['null']:
            if self.type == 0:
                mini_query = miniQueryNgo(self.ngos)
            else:
                mini_query = miniQueryLocalNgo(self.ngos)
            query += " and " + mini_query

        sql_query = text(query)
        result = db.engine.execute(sql_query, year=self.year)
        data = list()
        for row in result:
            data.append(ngoName(row[0]))

        return data

    def viewDataPartnerNgo(self):
        query = "select distinct(saving_group.partner_id)" \
                " from saving_group," \
                " province," \
                " district," \
                " sector," \
                " ngo" \
                " where saving_group.sector_id =sector.id" \
                " and sector.district_id = district.id" \
                " and district.province_id = province.id" \
                " and saving_group.partner_id = ngo.id" \
                " and saving_group.year = :year"

        if self.provinces != ['null']:
            mini_query = miniQueryProvince(self.provinces)
            query += " and " + mini_query

        if self.districts != ['null']:
            mini_query = miniQueryDistrict(self.districts)
            query += " and " + mini_query

        if self.sectors != ['null']:
            mini_query = miniQuerySector(self.sectors)
            query += " and " + mini_query

        if self.ngos != ['null']:
            if self.type == 0:
                mini_query = miniQueryNgo(self.ngos)
            else:
                mini_query = miniQueryLocalNgo(self.ngos)
            query += " and " + mini_query

        sql_query = text(query)
        result = db.engine.execute(sql_query, year=self.year)
        data = list()
        for row in result:
            data.append(ngoName(row[0]))

        return data


def miniQueryProvince(provinces):
    mini_query = "province.id IN ("
    for i, province in enumerate(provinces):
        if i == len(provinces) - 1:
            mini_query += province
        else:
            mini_query += province + ","

    mini_query += ")"

    return mini_query


def miniQueryDistrict(districts):
    mini_query = "district.id IN ("
    for i, district in enumerate(districts):
        if i == len(districts) - 1:
            mini_query += district
        else:
            mini_query += district + ","

    mini_query += ")"

    return mini_query


def miniQuerySector(sectors):
    mini_query = "sector.id IN ("
    for i, sector in enumerate(sectors):
        if i == len(sectors) - 1:
            mini_query += sector
        else:
            mini_query += sector + ","

    mini_query += ")"

    return mini_query


def miniQueryNgo(ngos):
    mini_query = "ngo.id IN ("
    for i, ngo in enumerate(ngos):
        if i == len(ngos) - 1:
            mini_query += ngo
        else:
            mini_query += ngo + ","

    mini_query += ")"

    return mini_query


def miniQueryLocalNgo(ngos):
    mini_query = "saving_group.funding_id IN ("
    for i, ngo in enumerate(ngos):
        if i == len(ngos) - 1:
            mini_query += ngo
        else:
            mini_query += ngo + ","

    mini_query += ")"

    return mini_query


def ngoName(id):
    sql = text('select name from ngo where id = :id')
    result = db.engine.execute(sql, id=id)
    for row in result:
        return row[0]


def convertNonType(val):
    try:
        val = int(val)
    except TypeError:
        val = 0
        return val
    return val