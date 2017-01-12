from marshmallow import Schema,fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    names = fields.String()
    username = fields.String()
    email = fields.String()
    phone = fields.String()
    user_role = fields.String()
    regDate = fields.Date()
    password = fields.String()
    gender = fields.String()
    update_key = fields.String()
    job_title = fields.String()
    ngo_id = fields.Integer()


class SavingGroupSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    year = fields.Integer()
    member_female = fields.Integer()
    member_male = fields.Integer()
    sector_id = fields.Integer()
    sector_name = fields.Str()
    district_name = fields.Str()
    regDate = fields.Date()


class AmountSchema(Schema):
    id = fields.Integer(dump_only=True)
    saving = fields.Float()
    borrowing = fields.Float()
    year = fields.Integer()
    sg_id = fields.Nested(SavingGroupSchema, required=True)


class NgoSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
    telephone = fields.Str()
    website = fields.Str()
    category = fields.Int()
    picture = fields.Str()
    address = fields.Str()


class SgsSchema(Schema):
    id = fields.Integer(dump_only=True)
    partner_id = fields.Nested(NgoSchema)
    funding_id = fields.Nested(NgoSchema)


class FilesSchema(Schema):
    id = fields.Int()
    original = fields.Str()
    save = fields.Str()
    filename = fields.Str()
    regDate = fields.Date()
    user_id = fields.Int()


class ProvinceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    code = fields.Str()
    keyword = fields.Str()


class DistrictSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    code = fields.Str()
    province_code = fields.Str()
    province_id = fields.Int()


class SectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    code = fields.Str()
    district_code = fields.Str()
    district_id = fields.Int()


class FinancialSchema(Schema):
    id = fields.Int(dump_only=True)
    branch_name = fields.Str()
    financial_name = fields.Str()
    sector_id = fields.Int()


class BankAgentSchema(Schema):
    id = fields.Int(dump_only=True)
    distribution = fields.Int()
    district_id = fields.Int()


class TelcoAgentSchema(Schema):
    id = fields.Int(dump_only=True)
    distribution = fields.Int()
    district_id = fields.Int()


class Population(Schema):
    id = fields.Int(dump_only=True)
    male = fields.Int()
    female = fields.Int()
    sector_id = fields.Int()



####### INITIALIZE ALL SCHEMA #######

user_schema = UserSchema()
users_schema = UserSchema(many=True)


sg_schema = SavingGroupSchema()
sgs_schema = SavingGroupSchema(many=True)

amount_schema = AmountSchema()
amounts_schema = AmountSchema(many=True)

ngo_schema = NgoSchema()
ngos_schema = NgoSchema(many=True)

sgfp_schema = SgsSchema()
sgfps_schema = SgsSchema(many=True)

file_schema = FilesSchema()
files_schema = FilesSchema(many=True)

province_schema = ProvinceSchema()
provinces_schema = ProvinceSchema(many=True)

district_schema = DistrictSchema()
districts_schema = DistrictSchema(many=True)

sector_schema = SectorSchema()
sectors_schema = SectorSchema(many=True)

financial_schema = FinancialSchema()
financials_schema = FinancialSchema(many=True)





