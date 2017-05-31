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
    upload = fields.Int()
    signup = fields.Int()
    ngo_id = fields.Int()
    ngo = fields.Nested(NgoSchema, only=["id","name","category"])


class ParamsSchema(Schema):
    id = fields.Int(dump_only=True)
    upload = fields.Int()
    signup = fields.Int()
    regDate = fields.Date()
    user_id = fields.Int()


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
    year = fields.Int()
    partner_id = fields.Int()
    funding_id = fields.Int()
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


class BankSchema(Schema):
    id = fields.Int(dump_only=True)
    count = fields.Int()
    name = fields.Str()
    year = fields.Int()
    sector_id = fields.Int()


class MfiSchema(Schema):
    id = fields.Int(dump_only=True)
    count = fields.Int()
    name = fields.Str()
    year = fields.Int()
    sector_id = fields.Int()


class UmurengeSacco(Schema):
    id = fields.Int(dump_only=True)
    count = fields.Int()
    name = fields.Str()
    year = fields.Int()
    sector_id = fields.Int()


class NonUmurengeSacco(Schema):
    id = fields.Int(dump_only=True)
    count = fields.Int()
    name = fields.Str()
    year = fields.Int()
    sector_id = fields.Int()


class BankAgentSchema(Schema):
    id = fields.Int(dump_only=True)
    count = fields.Int()
    year = fields.Int()
    district_id = fields.Int()


class TelcoAgentSchema(Schema):
    id = fields.Int(dump_only=True)
    count = fields.Int()
    year = fields.Int()
    district_id = fields.Int()


class Population(Schema):
    id = fields.Int(dump_only=True)
    male = fields.Int()
    female = fields.Int()
    sector_id = fields.Int()


class FinscopeSchema(Schema):
    id = fields.Int(dump_only=True)
    banked = fields.Int()
    other_formal = fields.Int()
    other_informal = fields.Int()
    excluded = fields.Int()
    year = fields.Int()
    district_id = fields.Int()



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

bank_schema = BankSchema()
banks_schema = BankSchema(many=True)

finscope_schema = FinscopeSchema()
finscopes_schema = FinscopeSchema(many=True)

param_schema = ParamsSchema()
params_schema = ParamsSchema(many=True)




