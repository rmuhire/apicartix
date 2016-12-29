from kenessa import Province, District


class Checker:

    def __init__(self, identifier):
        """if isinstance(data, list):
            self.identifier = identifier
            self.province = data[0]
            self.district = data[1].lower().title()
            self.sector = data[2]
            self.member = data[3]
            self.saved = data[4]
            self.borrow = data[5]
            self.status = {}
        else:
            self.value = str(data) """

        self.identifier = identifier

    def province(self):
        province = Province(self.identifier).province()
        if province is None:
            return False
        return True

    def district(self):
        district = District(self.identifier).district()
        if district is None:
            return False
        return True

    def sector(self):
        sect, dist = self.identifier
        district = District(dist).district()
        if district is not None:
            sectors = District(dist).sector()
            for sector in sectors:
                if sector['name'].lower() == sect.lower():
                    return True
        return True




    def member(self):
        '''if int(self.member) < 15 | int(self.member > 30):
            return False'''
        return True

    def saved(self):
        """if int(self.saved) < int(15 * 100):
            return False"""
        return True

    def borrow(self):
        """if int(self.saved) <= 0 & int(self.borrow) != 0:
            return False"""
        return True





    def checker(self):

        # Check Province
        province = Province(self.province).province()
        if province is not None:
            self.status['province'] = 1
        else:
            self.status['province'] = 0


        # Check District

        '''district = json.loads(District(str(self.district)).district())
        self.status['district'] = 0

        if district['district']:'''
        self.status['district'] = 1

        # check Sector
        '''self.status['sector'] = 0
        if self.status['district']:
            data = json.loads(District(str(self.district)).sector())
            sectors = data[str(self.district)]
            items = sectors[0]['sector']
            for item in items:
                if item['name'].lower() == str(self.sector.lower()): '''
        self.status['sector'] = 1
        try:
            self.status['member'] = 1
            if int(self.member) < 15 | int(self.member > 30):
                self.status['member'] = 0
        except ValueError:
            self.status['member'] = 0


        try:
            self.status['saved'] = 1
            if int(self.saved) < int(15 * 100):
                self.status['saved'] = 0
        except ValueError:
            self.status['saved'] = 1
            if not self.saved:
                self.status['saved'] = 0

        try:
            self.status['borrow'] = 1
            if int(self.saved) <= 0 & int(self.borrow) != 0:
                self.status['saved'] = 0
                self.status['borrow'] = 0
        except ValueError:
            self.status['borrow'] = 1
            if not self.borrow:
                self.status['borrow'] = 0

        return self.status

    def empty(self):
        if not self.identifier:
            return False
        else:
            return True































