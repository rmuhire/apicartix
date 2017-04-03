from app.controller.location import KenQuerydb


class Checker:

    def __init__(self, identifier):
        self.identifier = identifier

    def province(self):
        province = KenQuerydb(self.identifier).province()
        if province:
            return True
        return False

    def district(self):
        district = KenQuerydb(self.identifier).district()
        if district:
            return True
        return False

    def sector(self):
        sector = KenQuerydb(self.identifier).sector()
        if sector:
            return True
        return False

    def member(self):
        # try:
        #     int(self.identifier) < 10 | int(self.identifier) > 30:
        #         return False
        # except ValueError:
        #     return False
        return True

    def saved(self):
        # try:
        #     if int(self.identifier) < int(15 * 100):
        #         return False
        # except ValueError:
        #     if not self.identifier:
        #         return False

        return True

    def borrow(self):
        # saved, borrow = self.identifier
        # try:
        #     if int(saved) <= 0 & int(borrow) != 0:
        #         return False
        # except ValueError:
        #     if not borrow:
        #         return False
        return True

    def empty(self):
        if len(str(self.identifier)) > 0:
            return True
        return False

