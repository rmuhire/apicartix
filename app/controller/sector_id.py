from kenessa import District
import json


def sector_id(sector, district):
    district = district.lower().title()
    data = json.loads(District(str(district)).sector())
    sectors = data[str(district)]
    items = sectors[0]['sector']

    for item in items:
        if item['name'].lower() == str(sector.lower()):
            return item['id']

