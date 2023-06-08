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

class GetCategory(Schema):
    id = fields.Integer()
    name = fields.String()

class GetLocation(Schema):
    id = fields.Integer()
    country = fields.String()
    city = fields.String()

class CreateLocation(Schema):

    country = fields.String()
    city = fields.String()


class UserData(Schema):
    id = fields.Integer()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.Email(validate=validate.Email())
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    phone = fields.String(
        validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"))
    userStatus = fields.String(validate=validate.OneOf(["regular", "premium"]))
    idlocation = fields.Integer()
    isAdmin = fields.Boolean()

class LocalAdData(Schema):
    id = fields.Integer()
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrls = fields.String()
    user_id = fields.Integer()
    location_id = fields.Integer()

class PublicAdData(Schema):
    id = fields.Integer()
    title = fields.String()
    fk_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    photoUrl = fields.String()
    about = fields.String()
    user_id = fields.Integer()


class CreateUser(Schema):
    firstName = fields.String()
    lastName = fields.String()
    email = fields.Email(validate=validate.Email())
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    phone = fields.String(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"))
    userStatus = fields.String(validate=validate.OneOf(["regular", "premium"]))
    isAdmin = fields.Boolean()
    idlocation = fields.Integer()#fields.Nested(LocationData)

class GetUser(Schema):
    id = fields.Integer()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.Email(validate=validate.Email())
    phone = fields.String(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"))
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    userStatus = fields.String(validate=validate.OneOf(["regular", "premium"]))
    isAdmin = fields.Boolean()
    idlocation = fields.Integer()

class CreateLocalAd(Schema):
    title = fields.String()
    id_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrl = fields.String()
    location_id = fields.Integer()

class GetLocalAd(Schema):
    id = fields.Integer()
    title = fields.String()
    id_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrl = fields.String()
    user_id = fields.Integer()
    location_id = fields.Integer()

class CreatePublicAd(Schema):
    title = fields.String()
    id_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrl = fields.Raw(type='file')


class GetPublicAd(Schema):
    id=fields.Integer()
    title = fields.String()
    id_category = fields.Integer()
    status = fields.String(validate=validate.OneOf(["active", "closed", "confirmed"]))
    publishingDate = fields.DateTime()
    about = fields.String()
    photoUrl = fields.String()
    user_id = fields.Integer()