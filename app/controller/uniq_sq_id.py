def uniq_sg_id(intl_ngo_id, local_ngo_id, s_id, sg_name):
    sg_name = sg_name.replace(" ","_").lower()
    id = ''.join([intl_ngo_id,local_ngo_id, s_id, sg_name])

    return id


def uniq_id_amount(year_amount, sg_id):
    id = ''.join([year_amount, sg_id])
    return id
