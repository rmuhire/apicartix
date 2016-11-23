from xlrd import open_workbook
import psycopg2
import json


wb = open_workbook('svg.xls')
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols

    for r in range(0,1):
        vs=[]
        for c in range(number_of_columns):
            v = (sheet.cell(r,c).value)
            vs.append(v)

    items = []

    rows = []
    for row in range(1, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            try:
                value = str(int(value))

            except ValueError:
                pass
            finally:
                values.append(value)

        item = values
        items.append(item)

data=[]
hds=[]

for item in items:
    data.append(item)
    datas = json.dumps(data,sort_keys=True, indent=4)
print datas
for vd in vs:
    hds.append(vd)
print hds
