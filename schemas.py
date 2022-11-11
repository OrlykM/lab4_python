from marshmallow import Schema, fields, validate
from flask_bcrypt import Bcrypt, generate_password_hash
from marshmallow import ValidationError
from json import *

class LocationData(Schema):
    id = fields.Integer()
    country = fields.String()
    city = fields.String()

class CategoryData(Schema):
    id = fields.Integer()
    name = fields.String()

class UserData(Schema):
    id = fields.Integer()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.Email(validate=validate.Email())
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    phone = fields.String(
        validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"))
    userStatus = fields.String(validate=validate.OneOf(["regular", "premium"]))
    fk_location = fields.Integer()

class LocalAdData(Schema):
    id = fields.Integer()
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrls = fields.String()
    fk_user_id = fields.Integer()
    fk_location_id = fields.Integer()

class PublicAdData(Schema):
    id = fields.Integer()
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    fk_user_id = fields.Integer()

#fields.Nested(LocationData(only=('id')))

class CreateUser(Schema):
    firstName = fields.String()
    lastName = fields.String()
    email = fields.Email(validate=validate.Email())
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    phone = fields.String(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"))
    userStatus = fields.String(validate=validate.OneOf(["regular", "premium"]))
    fk_location_id = fields.Integer()#fields.Nested(LocationData)

class GetUser(Schema):
    firstName = fields.String()
    lastName = fields.String()
    email = fields.Email(validate=validate.Email())
    phone = fields.String(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"))
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    userStatus = fields.String(validate=validate.OneOf(["regular", "premium"]))
    fk_location_id = fields.Integer()

class CreateLocalAd(Schema):
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrls = fields.String()
    fk_user_id = fields.Integer()
    fk_location_id = fields.Integer()

class GetLocalAd(Schema):
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrls = fields.String()
    fk_user_id = fields.Integer()
    fk_location_id = fields.Integer()

class CreatePublicAd(Schema):
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    fk_user_id = fields.Integer()

class GetPublicAd(Schema):
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrls = fields.String()
    fk_user_id = fields.Integer()