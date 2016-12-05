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


class SavingGroupSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    year = fields.Integer()
    member_female = fields.Integer()
    member_male = fields.Integer()
    sector_id = fields.Integer()
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