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
    job_title = fields.String()
    ngo_id = fields.Integer()

user_schema = UserSchema()
users_schema = UserSchema(many = True)

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

class AmountSchema(Schema):
    id = fields.Integer(dump_only = True)
    saving = fields.Float()
    borrowing = fields.Float()
    year = fields.Integer()
    sg_id = fields.Nested(SavingGroupSchema, required=True)

amount_schema = AmountSchema()
amounts_schema = AmountSchema(many = True)


class NgoSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
    telephone = fields.Str()
    website = fields.Str()
    category = fields.Int()
    picture = fields.Str()
    address = fields.Str()


ngo_schema = NgoSchema()
ngos_schema = NgoSchema(many = True)


class SgsSchema(Schema):
    id = fields.Integer(dump_only = True)
    partner_id = fields.Integer()
    funding_id = fields.Integer()

sgfp_schema = SgsSchema()
sgfps_schema = SgsSchema(many = True)

class CoverSchema(Schema):
    id = fields.Integer(dump_only = True)
    ngo_id = fields.Integer()
    code = fields.Integer()

cov_schema = CoverSchema()
covs_schema = CoverSchema(many = True)
