from xlrd import open_workbook
import json




class Excellento:
    def __init__(self, filepath):
        self.filepath =filepath

    def exc_json(self):
        wb = open_workbook(self.filepath)
        for sheet in wb.sheets():
            number_of_rows = sheet.nrows
            number_of_columns = sheet.ncols

            for row in range(0, 1):
                header_sheet = []
                for col in range(number_of_columns):
                    header_cell = (sheet.cell(row, col).value)
                    header_sheet.append(header_cell)

            items = []

            for row in range(1, number_of_rows):
                data_json = {}
                for col in range(number_of_columns):
                    value = (sheet.cell(row, col).value)
                    try:
                        value = str(int(value))

                    except ValueError:
                        pass
                    finally:
                        data_json[header_sheet[col]] = value

                items.append(data_json)
        for item in items:

            svgs=SavingGroup(
                    name=item[0],
                    year=item[1],
                    member_female=item[2],
                    member_male=item[3],
                    sector_id=item[4],
                    regDate=datetime.datetime.utcnow()
                    )
            amt = Amount(
                    saving = item[7],
                    borrowing = item[8],
                    year = item[1],
                    sg_id = (items.index(item))+1
                    )
            fun=Funding.query.filter_by(name=item[5]).first()
            if fun:
                cd=Funding.query.filter_by(id=fun.id).first()
                if cd:
                    ab=cd
                else:
                    ab=""
            else:
                ab = ""

            par=Partner.query.filter_by(name=item[6]).first()
            if par:
                ef=Partner.query.filter_by(id=par.id).first()
                if ef:
                    fe=ef
                else:
                    fe=""
            else:
                fe = ""

            sgs=Sgs(
                funding_id=ab,
                partner_id=fe
                )

            db.session.add(sgs)
            db.session.add(amt)
            db.session.add(svgs)
            db.session.commit()

        return json.dumps(items,sort_keys=True, indent=4)
