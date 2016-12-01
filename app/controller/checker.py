from kenessa import Province, District
import json


class Checker:

    def __init__(self, data):
        self.province = data[0]
        self.district = data[1]
        self.sector = data[2]
        self.member = data[3]
        self.saved = data[4]
        self.borrow = data[5]
        self.status = {}

    def checker(self):

        # Check Province
        try:
            Province('East').province()
            self.status['province'] = 1
        except KeyError:
            self.status['province'] = 0

        # Check District

        try:
            District('Bugesera').district()
            self.status['district'] = 1
        except KeyError:
            self.status['district'] = 0

        # check Sector

        '''if self.status['district']:
            sectors = json.loads(District(self.district).sector())
            self.status['sector'] = 0
            for sector in sectors:
                if sector['name'].lower() == self.sector.lower():
                    self.status['sector'] = 1'''

        return self.status






























