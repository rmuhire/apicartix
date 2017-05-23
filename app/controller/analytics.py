from app.model.models import *
from sqlalchemy import text
from saving_year import creation_year


class MapAnalytics:
    def __init__(self):
        pass

    def provinceAnalytics(self):
        sql_province = text('select count(saving_group.name)'
                            ', sum(saving_group.member_female) '
                            ', sum(saving_group.member_male)'
                            ', sum(saving_group.borrowing)'
                            ', sum(saving_group.saving)'
                            ', province.name '
                            'from saving_group, sector, district, province '
                            'where sector.id = saving_group.sector_id AND '
                            'district.id = sector.district_id AND '
                            'province.id = district.province_id '
                            'group by province.name order by province.name')
        result = db.engine.execute(sql_province)
        province = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5]]
            province.append(data)

        """ bank data """
        sql_bank = text('select sum(bank.count),'
                        ' province.name from bank,'
                        ' sector,'
                        ' district,'
                        ' province'
                        ' where'
                        ' bank.sector_id = sector.id'
                        ' AND district.id = sector.district_id'
                        ' AND province.id = district.province_id'
                        ' group by province.name order by province.name')
        bank = runQuery(sql_bank)

        """ mfi data """
        sql_mfi = text('select sum(mfi.count),'
                       ' province.name'
                       ' from mfi, sector, district, province'
                       ' where mfi.sector_id = sector.id'
                       ' AND district.id = sector.district_id'
                       ' AND province.id = district.province_id'
                       ' group by province.name'
                       ' order by province.name')
        mfi = runQuery(sql_mfi)

        """ umurengo sacco """

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' province.name'
                          ' from umurenge_sacco,'
                          ' sector, district, province'
                          ' where umurenge_sacco.sector_id = sector.id'
                          ' AND district.id = sector.district_id'
                          ' AND province.id = district.province_id'
                          ' group by province.name order by province.name')

        usacco = runQuery(sql_usacco)

        """ non umurenge sacco """

        sql_nsacco = text('select sum(non_umurenge_sacco.count),'
                          ' province.name from non_umurenge_sacco,'
                          ' sector, district, province'
                          ' where non_umurenge_sacco.sector_id = sector.id AND'
                          ' district.id = sector.district_id AND'
                          ' province.id = district.province_id'
                          ' group by province.name order by province.name')
        nsacco = runQuery(sql_nsacco)

        """ bank agent """
        sql_bank_agent = text('select sum(bank_agent.count),'
                              ' province.name from bank_agent, district,'
                              ' province where bank_agent.district_id = district.id'
                              ' AND province.id = district.province_id'
                              ' group by province.name order by province.name')
        bank_agent = runQuery(sql_bank_agent)

        """ Telco Agent """
        sql_telco_agent = text('select sum(telco_agent.count), province.name'
                               ' from telco_agent, district, province'
                               ' where telco_agent.district_id = district.id'
                               ' AND province.id = district.province_id'
                               ' group by province.name order by province.name')
        telco_agent = runQuery(sql_telco_agent)
        return [province, bank, mfi, usacco, nsacco, bank_agent, telco_agent]

    def districtAnalytics(self):
        sql_district = text('select count(saving_group.name)'
                            ', sum(saving_group.member_female) '
                            ', sum(saving_group.member_male)'
                            ', sum(saving_group.borrowing)'
                            ', sum(saving_group.saving)'
                            ', district.name '
                            'from saving_group, sector, district '
                            'where sector.id = saving_group.sector_id AND '
                            'saving_group.borrowing != :x AND '
                            'saving_group.saving != :x AND '
                            'district.id = sector.district_id '
                            'group by district.name order by district.name')

        result = db.engine.execute(sql_district, x=-2)
        district = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5]]
            district.append(data)

        """ bank data """
        sql_bank = text('select sum(bank.count),'
                        ' district.name from bank,'
                        ' sector,'
                        ' district'
                        ' where'
                        ' bank.sector_id = sector.id'
                        ' AND district.id = sector.district_id'
                        ' group by district.name order by district.name')
        bank = runQuery(sql_bank)

        """ mfi data """
        sql_mfi = text('select sum(mfi.count),'
                       ' district.name'
                       ' from mfi, sector, district'
                       ' where mfi.sector_id = sector.id'
                       ' AND district.id = sector.district_id'
                       ' group by district.name'
                       ' order by district.name')
        mfi = runQuery(sql_mfi)

        """ umurengo sacco """

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' district.name'
                          ' from umurenge_sacco,'
                          ' sector, district'
                          ' where umurenge_sacco.sector_id = sector.id'
                          ' AND district.id = sector.district_id'
                          ' group by district.name order by district.name')

        usacco = runQuery(sql_usacco)

        """ non umurenge sacco """

        sql_nsacco = text('select sum(non_umurenge_sacco.count),'
                          ' district.name from non_umurenge_sacco,'
                          ' sector, district'
                          ' where non_umurenge_sacco.sector_id = sector.id AND'
                          ' district.id = sector.district_id'
                          ' group by district.name order by district.name')
        nsacco = runQuery(sql_nsacco)

        """ bank agent """
        sql_bank_agent = text('select sum(bank_agent.count),'
                              ' district.name from bank_agent, district'
                              ' where bank_agent.district_id = district.id'
                              ' group by district.name order by district.name')
        bank_agent = runQuery(sql_bank_agent)

        """ Telco Agent """
        sql_telco_agent = text('select sum(telco_agent.count), district.name'
                               ' from telco_agent, district'
                               ' where telco_agent.district_id = district.id'
                               ' group by district.name order by district.name')
        telco_agent = runQuery(sql_telco_agent)

        return [district, bank, mfi, usacco, nsacco, bank_agent, telco_agent]

    def sectorAnalytics(self):
        sql_district = text('select count(saving_group.name)'
                            ', sum(saving_group.member_female) '
                            ', sum(saving_group.member_male)'
                            ', sum(saving_group.borrowing)'
                            ', sum(saving_group.saving)'
                            ', sector.name'
                            ', sector.district_id '
                            'from saving_group, sector '
                            'where sector.id = saving_group.sector_id '
                            'AND saving_group.borrowing != :x AND '
                            'saving_group.saving != :x '
                            'group by sector.id order by sector.name')
        result = db.engine.execute(sql_district, x=-2)
        sector = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5], returnDistrict(row[6])]
            sector.append(data)

        """ bank data """
        sql_bank = text('select sum(bank.count),'
                        ' sector.name from bank,'
                        ' sector'
                        ' where'
                        ' bank.sector_id = sector.id'
                        ' group by sector.name order by sector.name')
        bank = runQuery(sql_bank)

        """ mfi data """
        sql_mfi = text('select sum(mfi.count),'
                       ' sector.name'
                       ' from mfi, sector'
                       ' where mfi.sector_id = sector.id'
                       ' group by sector.name'
                       ' order by sector.name')
        mfi = runQuery(sql_mfi)

        """ umurengo sacco """

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' sector.name'
                          ' from umurenge_sacco,'
                          ' sector'
                          ' where umurenge_sacco.sector_id = sector.id'
                          ' group by sector.name order by sector.name')

        usacco = runQuery(sql_usacco)

        """ non umurenge sacco """

        sql_nsacco = text('select sum(non_umurenge_sacco.count),'
                          ' sector.name from non_umurenge_sacco,'
                          ' sector'
                          ' where non_umurenge_sacco.sector_id = sector.id '
                          ' group by sector.name order by sector.name')
        nsacco = runQuery(sql_nsacco)

        return [sector, bank, mfi, usacco, nsacco]

    def json(self):
        province, bank, mfi, usacco, nsacco, bank_agent, telco_agent = MapAnalytics().provinceAnalytics()
        district, bank_d, mfi_d, usacco_d, nsacco_d, bank_agent_d, telco_agent_d = MapAnalytics().districtAnalytics()
        sector, bank_s, mfi_s, usacco_s, nsacco_s = MapAnalytics().sectorAnalytics()

        # Province

        provinces = []
        for i in range(len(province)):
            data = {}
            value = province[i]
            bank_val = bank[i]
            mfi_val = mfi[i]
            usacco_val = usacco[i]
            nsacco_val = nsacco[i]
            telco_agent_val = telco_agent[i]
            bank_agent_val = bank_agent[i]
            data['Province'] = returnProvince(value[5])
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            data['borrowing'] = value[3]
            data['saving'] = value[4]
            data['bank'] = bank_val[0]
            data['mfi'] = mfi_val[0]
            data['usacco'] = usacco_val[0]
            data['nsacco'] = nsacco_val[0]
            data['bank_agent'] = bank_agent_val[0]
            data['telco_agent'] = telco_agent_val[0]
            provinces.append(data)

        # District

        districts = []
        for i in range(len(district)):
            data = {}
            value = district[i]
            bank_val = bank_d[i]
            mfi_val = mfi_d[i]
            usacco_val = usacco_d[i]
            try:
                nsacco_val = nsacco_d[i]
            except IndexError:
                nsacco_val = [0,0]

            telco_agent_val = telco_agent_d[i]
            bank_agent_val = bank_agent_d[i]
            data['District'] = value[5].title()
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            data['borrowing'] = value[3]
            data['saving'] = value[4]
            data['bank'] = bank_val[0]
            data['mfi'] = mfi_val[0]
            data['usacco'] = usacco_val[0]
            data['nsacco'] = nsacco_val[0]
            data['bank_agent'] = bank_agent_val[0]
            data['telco_agent'] = telco_agent_val[0]
            districts.append(data)

        # Sector

        sectors = []
        for i in range(len(sector)):
            data = {}
            value = sector[i]
            try:
                bank_val = bank_s[i]
            except IndexError:
                bank_val = [0,0]
            try:
                mfi_val = mfi_s[i]
            except IndexError:
                mfi_val = [0,0]
            try:
                usacco_val = usacco_s[i]
            except IndexError:
                usacco_val = [0,0]

            try:
                nsacco_val = nsacco_s[i]
            except IndexError:
                nsacco_val = [0, 0]

            telco_agent_val = [0,0]
            bank_agent_val = [0,0]

            data['District'] = value[6].title()
            data['Sector'] = value[5].title()
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            data['borrowing'] = value[3]
            data['saving'] = value[4]
            data['bank'] = bank_val[0]
            data['mfi'] = mfi_val[0]
            data['usacco'] = usacco_val[0]
            data['nsacco'] = nsacco_val[0]
            data['bank_agent'] = bank_agent_val[0]
            data['telco_agent'] = telco_agent_val[0]
            sectors.append(data)

        return [provinces, districts, sectors]


class ChartAnalytics:
    def __init__(self, year):
        self.year = year

    # Membership per gender
    def membership(self):
        membership_sql = text('select sum(member_female)'
                              ', sum(member_male) from saving_group, sector'
                              ' where sector.id = saving_group.sector_id and saving_group.year = :year')
        result = db.engine.execute(membership_sql, year= self.year)

        val = []
        labels = ['Male Members', 'Female Members']
        for row in result:
            val = [row[0], row[1]]

        data = []
        item = {}
        item['values'] = val
        item['labels'] = labels
        item['type'] = 'pie'

        data.append(item)

        return data

    # SGS_status per Intl NGOs
    def sg_status(self):

        # Supervised query
        supervised_sql = text('select count(sg_status), partner_id from saving_group '
                              'WHERE sg_status = :val GROUP BY partner_id')
        result = db.engine.execute(supervised_sql, val='Supervised', year=self.year)
        supervised = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            supervised.append(data)

        # Graduated Query
        graduated_sql = text('select count(sg_status), partner_id from saving_group '
                              'WHERE sg_status = :val GROUP BY partner_id')
        result = db.engine.execute(graduated_sql, val='Graduated')
        graduated = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            graduated.append(data)

        supervised, graduated = renderStatusArray(supervised, graduated)

        # Supervised x y classification
        x = []
        y = []
        for item in supervised:
            x.append(item[1])
            y.append(item[0])

        # Json Supervised
        json_sup = {}
        json_sup['x'] = x
        json_sup['y'] = y
        json_sup['name'] = 'Supervised'
        json_sup['type'] = 'bar'

        # Graduated x y classification
        x = []
        y = []
        for item in graduated:
            x.append(item[1])
            y.append(item[0])

        json_grad = {}
        json_grad['x'] = x
        json_grad['y'] = y
        json_grad['name'] = 'Graduated'
        json_grad['type'] = 'bar'

        return [json_sup, json_grad]

    # SG Savings and Loans per Intl NGOs
    def savings_loans(self):

        # Savings query
        saving_sql = text('select sum(saving), partner_id from saving_group '
                          'where saving <> -1 '
                          'GROUP by partner_id')
        result = db.engine.execute(saving_sql)

        saving = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            saving.append(data)

        # Loans query
        loan_sql = text('select sum(borrowing), partner_id from saving_group '
                          'where saving <> -1 '
                          'GROUP by partner_id')
        result = db.engine.execute(loan_sql)
        loan = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            loan.append(data)

        # sort array
        saving = sortArray(saving)
        loan = sortArray(loan)

        #return [saving, loan]

        # Saving x y classification
        x = []
        y = []
        for item in saving:
            x.append(item[1])
            y.append(item[0])

        json_saving = dict()
        json_saving['x'] = x
        json_saving['y'] = y
        json_saving['name'] = 'Savings'
        json_saving['type'] = 'bar'

        # Loan x y classification
        x = []
        y = []
        for item in loan:
            x.append(item[1])
            y.append(item[0])

        json_loan = dict()
        json_loan['x'] = x
        json_loan['y'] = y
        json_loan['name'] = 'Loans'
        json_loan['type'] = 'bar'

        return [json_saving, json_loan]

    # Saving Group creation year
    def creation(self):
        years = creation_year()
        data = []
        for year in years:
            yearlist = list()
            year_sql = text('select count(id), partner_id from saving_group '
                            'where year_of_creation = :year '
                            'GROUP BY partner_id')
            result = db.engine.execute(year_sql, year=year)
            for row in result:
                val = [row[0], getNgoName(row[1])]
                yearlist.append(val)

            data.append(sortArray(yearlist))

        trace = []
        for i in range(len(data)):
            x = []
            y = []
            json = dict()
            for item in data[i]:
                x.append(item[1])
                y.append(item[0])
            json['x'] = x
            json['y'] = y
            json['name'] = years[i]
            json['type'] = 'bar'
            trace.append(json)

        return trace

    def savingPerIntNgo(self):
        sql = text('select count(saving_group.id),'
                   ' ngo.id,'
                   ' ngo.name'
                   ' from saving_group,'
                   ' ngo where saving_group.partner_id = ngo.id'
                   ' AND saving_group.year = 2014'
                   ' group by ngo.id')

        result = db.engine.execute(sql)
        values = list()
        labels = list()
        for row in result:
            values.append(row[0])
            labels.append(row[2])

        json = dict()
        json['values'] = values
        json['labels'] = labels
        json['type'] = 'pie'

        return [json]

    def localPerIntNgo(self):
        sql = text('select distinct(funding_id)'
                    ' from saving_group'
                    ' where year = 2014')
        result = db.engine.execute(sql)
        data = list()
        for row in result:
            funding_id = row[0]
            x = list()
            y = list()
            sql = text('select distinct(partner_id),'
                       ' count(id)'
                       ' from saving_group'
                       ' where funding_id = :funding_id'
                       ' group by partner_id')
            re = db.engine.execute(sql, funding_id=funding_id)
            for item in re:
                x.append(getNgoName(item[0]))
                y.append(item[1])
            json = dict()
            json['x'] = x
            json['y'] = y
            json['name'] = getNgoName(funding_id)
            json['type'] = 'bar'
            data.append(json)
        return data

    def sgFinancialInstitution(self):
        sql_sg = text('select count(saving_group.id),'
                      ' province.name'
                      ' from saving_group,'
                      ' sector, district,'
                      ' province where sector.id = saving_group.sector_id'
                      ' AND district.id = sector.district_id'
                      ' AND province.id = district.province_id'
                      ' group by province.name'
                      ' order by province.name')
        result = db.engine.execute(sql_sg)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        # Bank Data
        sql_banks = text('select sum(bank.count),'
                         ' province.name'
                         ' from bank,'
                         ' sector,'
                         ' district,'
                         ' province'
                         ' where sector.id = bank.sector_id'
                         ' AND district.id = sector.district_id'
                         ' AND province.id = district.province_id'
                         ' group by province.name order'
                         ' by province.name')
        result = db.engine.execute(sql_banks)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_bank = dict()
        json_bank['x'] = x
        json_bank['y'] = y
        json_bank['name'] = 'Banks'
        json_bank['type'] = 'bar'


        # mfi
        sql_mfi = text('select sum(mfi.count),'
                       ' province.name'
                       ' from mfi, sector, district, province '
                       'where sector.id = mfi.sector_id AND'
                       ' district.id = sector.district_id AND'
                       ' province.id = district.province_id group by'
                       ' province.name order by province.name')
        result = db.engine.execute(sql_mfi)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_mfi = dict()
        json_mfi['x'] = x
        json_mfi['y'] = y
        json_mfi['name'] = 'MFIs'
        json_mfi['type'] = 'bar'

        # umurenge sacco

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' province.name'
                          ' from umurenge_sacco, sector, district, province'
                          ' where sector.id = umurenge_sacco.sector_id AND'
                          ' district.id = sector.district_id AND'
                          ' province.id = district.province_id'
                          ' group by province.name'
                          ' order by province.name')
        result = db.engine.execute(sql_usacco)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_usacco = dict()
        json_usacco['x'] = x
        json_usacco['y'] = y
        json_usacco['name'] = 'Umurenge Sacco'
        json_usacco['type'] = 'bar'

        # Non - Umurenge Sacco

        sql_nusacco = text('select sum(non_umurenge_sacco.count),'
                           ' province.name'
                           ' from non_umurenge_sacco, sector, district, province'
                           ' where sector.id = non_umurenge_sacco.sector_id'
                           ' AND district.id = sector.district_id '
                           'AND province.id = district.province_id '
                           'group by province.name '
                           'order by province.name')
        result = db.engine.execute(sql_nusacco)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_nusacco = dict()
        json_nusacco['x'] = x
        json_nusacco['y'] = y
        json_nusacco['name'] = 'Non-Umurenge Sacco'
        json_nusacco['type'] = 'bar'

        return [json_sg, json_bank, json_mfi, json_usacco, json_nusacco]

    def sgTelcoAgent(self):
        # telco agent
        sql_telco = text('select sum(telco_agent.count),'
                         ' province.name'
                         ' from telco_agent, province, district'
                         ' where telco_agent.district_id = district.id '
                         'and district.province_id = province.id '
                         'group by province.name '
                         'order by province.name')
        result = db.engine.execute(sql_telco)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_telco = dict()
        json_telco['x'] = x
        json_telco['y'] = y
        json_telco['name'] = 'Telco Agents'
        json_telco['type'] = 'bar'

        # bank agent
        sql_bank = text('select sum(bank_agent.count),'
                         ' province.name'
                         ' from bank_agent, province, district'
                         ' where bank_agent.district_id = district.id '
                         'and district.province_id = province.id '
                         'group by province.name '
                         'order by province.name')
        result = db.engine.execute(sql_bank)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_bank = dict()
        json_bank['x'] = x
        json_bank['y'] = y
        json_bank['name'] = 'Bank Agents'
        json_bank['type'] = 'bar'

        # sg

        sql_sg = text('select count(saving_group.id),'
                      ' province.name'
                      ' from saving_group,'
                      ' sector, district,'
                      ' province where sector.id = saving_group.sector_id'
                      ' AND district.id = sector.district_id'
                      ' AND province.id = district.province_id'
                      ' group by province.name'
                      ' order by province.name')
        result = db.engine.execute(sql_sg)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        return [json_sg, json_telco, json_bank]

    def finscope(self):
        sg_2012 = text('select sum(member_female), sum(member_male) '
                  'from saving_group'
                  ' where year_of_creation = 2012')
        result = db.engine.execute(sg_2012)
        x = list()
        y = list()
        for row in result:
            sum_sg_2012 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs vs Finscope 2012')
            y.append(sum_sg_2012)

        sg_2015 = text('select sum(member_female),'
                       ' sum(member_male)'
                  ' from saving_group'
                  ' where year_of_creation = 2015')
        result = db.engine.execute(sg_2015)
        for row in result:
            sum_sg_2015 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs vs Finscope 2015')
            y.append(sum_sg_2015)

        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        o_informal_2012 = text('select sum(other_informal)'
                               ' from finscope where year = 2012')
        result = db.engine.execute(o_informal_2012)
        x = list()
        y = list()
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2012
            x.append('SGs vs Finscope 2012')
            y.append(remain)

        o_informal_2015 = text('select sum(other_informal)'
                               ' from finscope where year = 2012')
        result = db.engine.execute(o_informal_2015)
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2015
            x.append('SGs vs Finscope 2015')
            y.append(remain)

        json_other = dict()
        json_other['x'] = x
        json_other['y'] = y
        json_other['name'] = 'Other Informal'
        json_other['type'] = 'bar'

        # Excluded data
        exluded_2012 = text('select sum(excluded) from finscope where year = 2012')
        result = db.engine.execute(exluded_2012)
        x = list()
        y = list()
        for row in result:
            x.append('SGs vs Finscope 2012')
            y.append(row[0])

        exluded_2015 = text('select sum(excluded) from finscope where year = 2015')
        result = db.engine.execute(exluded_2015)
        for row in result:
            x.append('SGs vs Finscope 2015')
            y.append(row[0])

        json_excluded = dict()
        json_excluded['x'] = x
        json_excluded['y'] = y
        json_excluded['name'] = 'Excluded'
        json_excluded['type'] = 'bar'

        return [json_sg, json_other, json_excluded]

    def finscope_sg(self):
        sg_2012 = text('select sum(member_female), sum(member_male) '
                       'from saving_group'
                       ' where year_of_creation = 2012')
        result = db.engine.execute(sg_2012)
        x = list()
        y = list()
        for row in result:
            sum_sg_2012 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs 2012')
            y.append(sum_sg_2012)

        o_informal_2012 = text('select sum(other_informal)'
                               ' from finscope where year = 2012')
        result = db.engine.execute(o_informal_2012)
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2012
            x.append('Other Informal 2012')
            y.append(remain)

        json_2012 = dict()
        json_2012['values'] = y
        json_2012['labels'] = x
        json_2012['type'] = 'pie'

        """ 2015  """
        sg_2015 = text('select sum(member_female), sum(member_male) '
                       'from saving_group'
                       ' where year_of_creation = 2015')
        result = db.engine.execute(sg_2015)
        x = list()
        y = list()
        for row in result:
            sum_sg_2015 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs 2015')
            y.append(sum_sg_2015)

        o_informal_2015 = text('select sum(other_informal)'
                               ' from finscope where year = 2015')
        result = db.engine.execute(o_informal_2015)
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2015
            x.append('Other Informal 2015')
            y.append(remain)

        json_2015 = dict()
        json_2015['values'] = y
        json_2015['labels'] = x
        json_2015['type'] = 'pie'

        return [json_2012, json_2015]

    def finscope_all(self, year):
        finscope = text('select sum(finscope.banked), sum(finscope.other_formal),'
                             ' sum(finscope.other_informal), sum(finscope.excluded),'
                             ' province.name from finscope, province,'
                             ' district where finscope.district_id = district.id'
                             ' and province.id = district.province_id'
                             ' and finscope.year = :year'
                             ' group by province.name order by province.name')
        result = db.engine.execute(finscope, year=year)
        x = list()
        banked = list()
        other_formal = list()
        other_informal = list()
        excluded = list()
        for row in result:
            x.append(row[4])
            banked.append(row[0])
            other_formal.append(row[1])
            other_informal.append(row[2])
            excluded.append(row[3])

        sgs = text('select sum(saving_group.member_female),'
                        ' sum(saving_group.member_male), province.name'
                        ' from saving_group, province, district, sector'
                        ' where saving_group.sector_id = sector.id'
                        ' and sector.district_id = district.id'
                        ' and district.province_id = province.id'
                        ' and saving_group.year_of_creation = :year'
                        ' group by province.name order by province.name')

        result = db.engine.execute(sgs, year=year)
        sg = list()
        for row in result:
            sg.append(convertNonType(row[0]) + convertNonType(row[1]))


        """ JSon Banked """
        json_banked = dict()
        json_banked['x'] = x
        json_banked['y'] = banked
        json_banked['name'] = 'Banked'
        json_banked['type'] = 'bar'

        """ Json Other Formal """
        json_other_formal = dict()
        json_other_formal['x'] = x
        json_other_formal['y'] = other_formal
        json_other_formal['name'] = 'Other Formal'
        json_other_formal['type'] = 'bar'

        """ Json Other informal """
        json_other_informal = dict()
        json_other_informal['x'] = x
        json_other_informal['y'] = other_informal
        json_other_informal['name'] = 'Other Infomal'
        json_other_informal['type'] = 'bar'

        """ Json Excluded """
        json_excluded = dict()
        json_excluded['x'] = x
        json_excluded['y'] = excluded
        json_excluded['name'] = 'Excluded'
        json_excluded['type'] = 'bar'

        """ Json SGs """
        json_sgs = dict()
        json_sgs['x'] = x
        json_sgs['y'] = sg
        json_sgs['name'] = 'SGs'
        json_sgs['type'] = 'bar'

        """ Calculate other informal """
        val = list()
        for i in range(len(sg)):
            val.append(convertNonType(other_informal[i]) - convertNonType(sg[i]))

        json_other_informal['y'] = val

        return [json_banked, json_other_formal, json_other_informal, json_excluded, json_sgs]

        """ Next merge SGs array for substraction with other_informal to get the real value of 
         other informal"""





class NumberAnalytics:
    def __init__(self, year):
        self.year = year

    def numbers(self):
        sql_number =  text('select count(id),'
                           ' sum(member_female),'
                           ' sum(member_male),'
                           ' sum(saving),'
                           ' sum(borrowing)'
                           ' from saving_group'
                           ' where year = :year')
        result = db.engine.execute(sql_number, year = self.year)
        if result:
            for row in result:
                if row[1] is None:
                    return [0,0,0,0]
                data = [row[0],row[1] + row[2], row[3], row[4]]
            return data


def convertNonType(val):
    try:
        val = int(val)
    except TypeError:
        val = 0
        return val
    return val


def returnProvince(name):
    val = ['kigali', 'north', 'south', 'west', 'east']
    data = ['Kigali City', 'Northern', 'Southern', 'Western', 'Eastern']

    for i in range(len(val)):
        if name == val[i]:
            return data[i]


def returnDistrict(id):
    district = text('select name from district where id = :id')
    result = db.engine.execute(district, id=id)

    for row in result:
        return row[0]


def renderStatusArray(supervised, graduated):
    i = 0
    for x in graduated:
        for y in supervised:
            if x[1] == y[1]:
                i = 1
            val = x[1]
        if i == 0:
            supervised.append([0, val])
        i = 0

    i = 0
    for x in supervised:
        for y in graduated:
            if x[1] == y[1]:
                i = 1
            val = x[1]
        if i == 0:
            graduated.append([0, val])
        i = 0

    return [sortArray(supervised),sortArray(graduated)]


def sortArray(list):
    sorted_array =  sorted(list, key=lambda x: x[1])
    return sorted_array


def getNgoName(id):
    ngo = text('select name from ngo where id = :id')
    result = db.engine.execute(ngo, id=id)
    for row in result:
        return row[0]


def runQuery(query):
    result = db.engine.execute(query)
    data = list()
    for row in result:
        data.append([row[0], row[1]])

    return data


