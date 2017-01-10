from kenessa import Province, District


class Checker:

    def __init__(self, identifier):
        self.identifier = identifier

    def province(self):
        """province = Province(self.identifier).province()
        if province is None:
            return False"""
        return True

    def district(self):
        """district = District(self.identifier).district()
        if district is None:
            return False"""
        return True

    def sector(self):
        """
        sect, dist = self.identifier
        district = District(dist).district()
        if district is not None:
            sectors = District(dist).sector()
            for sector in sectors:
                if sector['name'].lower() == sect.lower():
                    return True """
        return True

    def member(self):
        try:
            if int(self.identifier) < 15 | int(self.identifier > 30):
                return False
        except ValueError:
            return False
        return True

    def saved(self):
        try:
            if int(self.identifier) < int(15 * 100):
                return False
        except ValueError:
            if not self.identifier:
                return False

        return True

    def borrow(self):
        saved, borrow = self.identifier
        try:
            if int(saved) <= 0 & int(borrow) != 0:
                return False
        except ValueError:
            if not borrow:
                return False
        return True

    def empty(self):
        if len(str(self.identifier)) > 0:
            return True
        return False

