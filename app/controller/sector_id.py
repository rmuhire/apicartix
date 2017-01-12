from kenessa import District


def sector_id(sector, district):
    district = district.lower().title()
    data = District(str(district)).sector()

    for item in data:
        if item['name'].lower() == str(sector.lower()):
            return item['id']

