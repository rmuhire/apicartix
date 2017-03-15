from app import *
from app.model.models import *
from sqlalchemy import text


def provinceAnalytics():
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
                        'group by province.id')
    result = db.engine.execute(sql_province)
    province = []
    for row in result:
        data = [row[0], row[1], row[2], row[3], row[4], row[5]]
        province.append(data)

    return province


def districtAnalytics():
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


def sectorAnalytics():
    sql_district = text('select count(saving_group.name)'
                        ', sum(saving_group.member_female) '
                        ', sum(saving_group.member_male)'
                        ', sum(saving_group.borrowing)'
                        ', sum(saving_group.saving)'
                        ', sector.name '
                        'from saving_group, sector '
                        'where sector.id = saving_group.sector_id '
                        'AND saving_group.borrowing != :x AND '
                        'saving_group.saving != :x '
                        'group by sector.id')
    result = db.engine.execute(sql_district, x=-1)
    sector = []
    for row in result:
        data = [row[0], row[1], row[2], row[3], row[4], row[5]]
        sector.append(data)

    return sector
