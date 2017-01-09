from xlrd import open_workbook
import json
from saving_year import saving_year


class Excellento:

    def __init__(self, filepath):
        self.filepath = filepath
        self.wb = open_workbook(self.filepath)

    def json(self):
        for sheet in self.wb.sheets():
            rows = sheet.nrows
            columns = sheet.ncols

            for row in range(0, 1):
                header_sheet = []
                for col in range(columns):
                    if col == 11:
                        data = sheet.cell(row, col).value
                        val = saving_year(data)
                        header_sheet.append(val[1])
                    elif col == 12:
                        data = sheet.cell(row, col).value
                        val = saving_year(data)
                        header_sheet.append(val[2])
                    else:
                        header_cell = sheet.cell(row, col).value.replace(" ","_").replace("-","")
                        header_sheet.append(header_cell.lower())

            year = val[0]

            items = []

            for row in range(1, rows):
                data_json = {}
                for col in range(columns):
                    value = sheet.cell(row, col).value
                    try:
                        value = str(int(value))

                    except ValueError:
                        pass
                    finally:
                        data_json[header_sheet[col]] = value
                data_json["year_amount"] = year
                items.append(data_json)

        return items






