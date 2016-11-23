from xlrd import open_workbook
import psycopg2
import json


wb = open_workbook('svg.xls')
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols

    for row in range(0,1):
        header_sheet = []
        for col in range(number_of_columns):
            header_cell = (sheet.cell(row,col).value)
            header_sheet.append(header_cell)

    items = []

    for row in range(1, number_of_rows):
        data_json = {}
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            try:
                value = str(int(value))

            except ValueError:
                pass
            finally:
                data_json[header_sheet[col]] = value



        items.append(data_json)
print json.dumps(items,sort_keys=True, indent=4)
