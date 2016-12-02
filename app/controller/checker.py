from kenessa import Province, District
import json


class Checker:

    def __init__(self, data):
        self.province = data[0]
        self.district = data[1].lower().title()
        self.sector = data[2]
        self.member = data[3]
        self.saved = data[4]
        self.borrow = data[5]
        self.status = {}

    def checker(self):

        # Check Province

        province = json.loads(Province(str(self.province)).province())
        self.status['province'] = 0
        if province['province']:
            self.status['province'] = 1


        # Check District

        district = json.loads(District(str(self.district)).district())
        self.status['district'] = 0

        if district['district']:
            self.status['district'] = 1

        # check Sector
        self.status['sector'] = 0
        if self.status['district']:
            data = json.loads(District(str(self.district)).sector())
            sectors = data[str(self.district)]
            items = sectors[0]['sector']
            for item in items:
                if item['name'].lower() == str(self.sector.lower()):
                    self.status['sector'] = 1

        self.status['member'] = 1
        if int(self.member) < 15 | int(self.member > 30):
            self.status['member'] = 0

        try:
            self.status['saved'] = 1
            if int(self.saved) < int(15 * 100):
                self.status['saved'] = 0
        except ValueError:
            self.status['saved'] = 1

        try:
            self.status['borrow'] = 1
            if int(self.saved) <= 0 & int(self.borrow) != 0:
                self.status['saved'] = 0
                self.status['borrow'] = 0
        except ValueError:
            self.status['borrow'] = 1

        return self.status
































