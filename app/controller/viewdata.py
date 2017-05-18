from app.model.models import *
from sqlalchemy import text
import xlwt
from app.controller.uniqid import uniqid


class ViewData:
    def __init__(self, province, district, sector, ngo, year, type):
        self.provinces = province.split(",")
        self.districts = district.split(",")
        self.sectors = sector.split(",")
        self.ngos = ngo.split(",")
        self.year = int(year)
        self.type = type

    def queryDownload(self):
        query = "select saving_group.name, " \
                "saving_group.year, " \
                "saving_group.member_female, " \
                "saving_group.member_male, " \
                "saving_group.sector_id, " \
                "saving_group.sg_status, " \
                "saving_group.borrowing, " \
                "saving_group.funding_id, " \
                "saving_group.partner_id, " \
                "saving_group.year_of_creation, " \
                "saving_group.saving "\
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

        return query



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


class DownloadExcel:
    def __init__(self, query, year):
        self.query = query
        self.year = year

    def download(self):
        sql = text(self.query)
        result = db.engine.execute(sql, year=self.year)
        data = list()
        for row in result:
            province, district, sector = getLocation(row[4])
            tot=row[2]+row[3]
            data.append(
                [
                    province,
                    district,
                    sector,
                    row[0],
                    row[9],
                    tot,
                    row[2],
                    row[3],
                    row[7],
                    row[8],
                    row[5],
                    checkNA(row[6]),
                    checkNA(row[10])
                ]
            )

        headers =[
            'Province',
            'District',
            'Sector',
            'Saving Group name',
            'SGs Year of creation',
            'SGs Members Total',
            'SGs Members - Female',
            'SGs Members - Male',
            'Funding NGO',
            'Partner NGO',
            'SGs Status',
            'Saved Amount as of December '+self.year+' (In Rwf)',
            'Outstanding Loans as of December '+self.year+' (In Rwf)'
        ]

        wb = xlwt.Workbook()
        sg = wb.add_sheet('Saving Group')

        for row in range(1):
            for col in range(len(headers)):
                sg.write(row, col, headers[col])

        for row in range(1, len(data)):
            item = data[row]
            for col in range(len(headers)):
                sg.write(row, col, item[col])

        filename = uniqid() + "saving_group.xls"
        location ='/Users/muhireremy/cartix/downloads/'+filename
        wb.save(location)
        return location


def checkNA(amount):
    if amount == -1:
        return 'N/A'
    return amount


def getLocation(sector_id):
    sql = text("select province.name, district.name, "
               "sector.name "
               "from province, district, sector "
               "where province.id = district.province_id "
               "and sector.district_id = district.id "
               "and sector.id = :sector_id")
    result = db.engine.execute(sql, sector_id=sector_id)
    for row in result:
        return [row[0], row[1], row[2]]


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