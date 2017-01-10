from app.model.models import *
from sqlalchemy.exc import IntegrityError


class Ken:

    def __init__(self, json):
        self.json = json

    def province(self):
        for data in self.json:
            try:
                province = Province(
                    id=data['id'],
                    name=data['name'],
                    code=data['code'],
                    keyword=data['keywords']
                )
                db.session.add(province)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        return True

    def district(self):
        for data in self.json:
            try:
                district = District(
                    id=data['id'],
                    name=data['name'],
                    code=data['code'],
                    province_code=data['province_code'],
                    province_id=data['province_id']
                )
                db.session.add(district)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        return True

    def sector(self):
        for data in self.json:
            try:
                sector = Sector(
                    id=data['id'],
                    name=data['name'],
                    code=data['code'],
                    district_code=data['district_code'],
                    district_id=data['district_id']
                )
                db.session.add(sector)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        return True