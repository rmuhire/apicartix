from app.model.models import *
from app.controller.exellento import Excellento
from sqlalchemy.exc import IntegrityError
import xlwt

class Excellentodb:
    def __init__(self, file):
        self.file = file
        self.json_data = Excellento(self.file).json()

    def todb(self):
        for data in self.json_data:
            try:
                saving = SavingGroup(
                    name=data['saving_group_name'],
                    year=data['sgs_year_of_creation'],
                    member_female=data['sgs_members__female'],
                    member_male=data['sgs_members__male'],
                    sector_id=data['sector_code'],
                    regDate=None
                )
                db.session.add(saving)
                db.session.commit()
            except IntegrityError:
                db.session().rollback()
                saving = SavingGroup.query.filter_by(name=data['saving_group_name']).first()

            # Amount

            saving_amount = data['saved_amount_as_of_december_2014']
            if data['saved_amount_as_of_december_2014'] == 'N/A':
                saving_amount = -1

            borrowing_amount = data['outstanding_loans_as_of_december_2014']
            if data['outstanding_loans_as_of_december_2014'] == 'N/A':
                borrowing_amount = -1

            amount = Amount(
                saving= saving_amount,
                borrowing=borrowing_amount,
                year=2014,
                sg_id=saving.id
            )

            db.session.add(amount)
            db.session.commit()

            # International NGO

            try:
                ngo = Ngo(
                    name=data['funding_ngo'],
                    email=None,
                    telephone=None,
                    website=None,
                    category='funding_ngo',
                    picture=None,
                    address=None,
                    cp_name=None,
                    cp_email=None,
                    cp_telephone=None,
                    username=None,
                    password=None
                )

                db.session.add(ngo)
                db.session.commit()
                intl_ngo_id = ngo.id


            except IntegrityError:
                db.session().rollback()
                ngo = Ngo.query.filter_by(name=data['funding_ngo']).first()
                intl_ngo_id = ngo.id



            # Local NGO


            try:
                ngo = Ngo(
                    name=data['partner_ngo'],
                    email=None,
                    telephone=None,
                    website=None,
                    category='partner_ngo',
                    picture=None,
                    address=None,
                    cp_name=None,
                    cp_email=None,
                    cp_telephone=None,
                    username=None,
                    password=None
                )

                db.session.add(ngo)
                db.session.commit()

                local_ngo_id = ngo.id

            except IntegrityError:
                db.session().rollback()
                ngo = Ngo.query.filter_by(name=data['partner_ngo']).first()
                local_ngo_id = ngo.id

            # SGS

            sgs = Sgs(
                partner_id=local_ngo_id,
                funding_id=intl_ngo_id
            )

            db.session.add(sgs)
            db.session.commit()

        return 1

    def toexcel(self):


        book = xlwt.Workbook()

        # add new colour to palette and set RGB colour value
        xlwt.add_palette_colour("custom_colour", 0x21)
        book.set_colour_RGB(0x21, 255,0,0)

        # now you can use the colour in styles
        sheet1 = book.add_sheet('Sheet 1')
        style = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')

        sheet1.write(1, 4, 'Some text', style)
        sheet1.write(0, 2, 'Wrong', style)

        book.save('test.xls')



