from marshmallow import Schema,fields


class NgoSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
    telephone = fields.Str()
    website = fields.Str()
    category = fields.Int()
    picture = fields.Str()
    address = fields.Str()


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
    ngo = fields.Nested(NgoSchema, only=["id","name"])


class SavingGroupSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    year_of_creation = fields.Integer()
    member_female = fields.Integer()
    member_male = fields.Integer()
    sector_id = fields.Integer()
    sg_status = fields.Str()
    saving = fields.Float()
    borrowing = fields.Float()
    year = fields.Date()
    partner = fields.Nested(NgoSchema, only=["id","name"])
    funding = fields.Int(NgoSchema, only=["id","name"])
    regDate = fields.Date()


class FilesSchema(Schema):
    id = fields.Int()
    original = fields.Str()
    saved = fields.Str()
    filename = fields.Str()
    regDate = fields.Date()
    status = fields.Int()
    size = fields.Int()
    user_id = fields.Int()
    user = fields.Nested(UserSchema, only=["id","names", "ngo"])


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

ngo_schema = NgoSchema()
ngos_schema = NgoSchema(many=True)

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





