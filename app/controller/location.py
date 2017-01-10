from app.model.models import *
from sqlalchemy.exc import IntegrityError
from app.model.schema import *


class Kendb:

    def __init__(self, json):
        self.json = json

    def province(self):
        for data in self.json:
            try:
                key = data['keywords']
                keywords = ','.join(key)
                province = Province(
                    id=data['id'],
                    name=data['name'].lower(),
                    code=data['code'],
                    keyword=keywords.lower()
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
                    name=data['name'].lower(),
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
                    name=data['name'].lower(),
                    code=data['code'],
                    district_code=data['district_code'],
                    district_id=data['district_id']
                )
                db.session.add(sector)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        return True


class KenQuerydb:

    def __init__(self, data):
        self.data = data.replace(" ", "").lower()

    def province(self):
        province = Province.query.all()
        result = provinces_schema.dump(province)
        for province in result.data:
            keywords = province['keyword'].lower().split(",")
            if self.data in keywords:
                return True
        return False

    def district(self):
        district = District.query.filter_by(name=self.data).first()
        if district:
            return True
        return False

    def sector(self):
        sector = Sector.query.filter_by(name=self.data).first()
        if sector:
            return True
        return False
