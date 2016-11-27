from xlrd import open_workbook
import json



class Excellento:
    def __init__(self, filepath):
        self.filepath =filepath
        self.wb = open_workbook(self.filepath)

    def json(self):
        for sheet in self.wb.sheets():
            rows = sheet.nrows
            columns = sheet.ncols

            for row in range(0, 1):
                header_sheet = []
                for col in range(columns):
                    header_cell = (sheet.cell(row, col).value)
                    header_sheet.append(header_cell)

            items = []

            for row in range(1, rows):
                data_json = {}
                for col in range(columns):
                    value = (sheet.cell(row, col).value)
                    try:
                        value = str(int(value))

                    except ValueError:
                        pass
                    finally:
                        data_json[header_sheet[col]] = value

                items.append(data_json)
        return json.dumps(items,sort_keys=True, indent=4)






