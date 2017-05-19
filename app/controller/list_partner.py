def litPartnerNgo(items):
    uniqueList = {item['partner_id']: item for item in items}
    partner_id = []
    for id in uniqueList:
        partner_id.append(id)

    return partner_id


