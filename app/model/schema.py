from marshmallow import Schema,fields


class SavingGroupSchema(Schema):
    id = fields.Integer(dump_only = True)
    name = fields.String()
    year = fields.Integer()
    member_female = fields.Integer()
    member_male = fields.Integer()
    sector_id = fields.Integer()
    regDate = fields.Date()

sg_schema = SavingGroupSchema()
sgs_schema = SavingGroupSchema(many = True)

class Amount(Schema):
    id = fields.Integer(dump_only = True)
    saving = fields.Float()
    borrowing = fields.Float()
    year = fields.Integer()
    sg_id=fields.Nested(SavingGroupSchema)

amount_schema = Amount()
amounts_schema = Amount(many = True)

class FundingSchema(Schema):
    id = fields.Integer(dump_only = True)
    name = fields.String()
    email = fields.String()
    telephone = fields.String()
    website = fields.String()
    picture = fields.String()
    address = fields.String()
    cp_name = fields.String()
    cp_email = fields.String()
    cp_telephone = fields.String()

funding_schema = FundingSchema()
fundings_schema = FundingSchema(many = True)

class PartnerSchema(Schema):
    id = fields.Integer(dump_only = True)
    name = fields.String()
    email = fields.String()
    telephone = fields.String()
    website = fields.String()
    picture = fields.String()
    address = fields.String()
    cp_name = fields.String()
    cp_email = fields.String()
    cp_telephone = fields.String()

partner_schema = PartnerSchema()
partners_schema = PartnerSchema(many = True)


class SgsSchema(Schema):
    id = fields.Integer(dump_only = True)
    partner_id = fields.Nested(PartnerSchema)
    funding_id = fields.Nested(FundingSchema)

sgfp_schema = SgsSchema()
sgfps_schema = SgsSchema(many = True)
