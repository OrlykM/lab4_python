from flask import Blueprint, jsonify, request, make_response
import db_utils
from db_utils import *
from schemas import *
from models import *
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import generate_password_hash, check_password_hash

api_blueprint = Blueprint('api', __name__)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    user = db_utils.get_entry_by_email(User, email)
    if check_password_hash(user.password, password):
        return email
    return None


def admin_required(func):
    def wrapper(*args, **kwargs):
        email = auth.current_user()
        user = db_utils.get_entry_by_email(User, email)
        if user.isAdmin == 1:
            return func(*args, **kwargs)
        else:
            response = make_response(jsonify({"error": f"User must be an admin to use {func.__name__}."}))
            response.status_code = 401
            return response

    wrapper.__name__ = func.__name__
    return wrapper


@api_blueprint.route("/user/login")
@auth.verify_password
def login(email, password):

    user = db_utils.get_entry_by_email(User, email)
    if user == 404:
        return False
    if check_password_hash(user.password, password):
        return True
    return False


@api_blueprint.route('/user', methods=['POST'])
def create_user():
    try:
        user_data = CreateUser().load(request.json)
        if len(user_data) < 7:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response
        if user_data['isAdmin'] == 1:
            response = make_response('Error: only admin can create other admin')
            response.status_code = 410
            return response
        user = db_utils.create_usr(phn=user_data['phone'], eml=user_data['email'],
                                   location=user_data['idlocation'], stats=user_data['userStatus'], **user_data)
        if user == 405:
            response = make_response(jsonify("Duplicate phone or email"))
            response.status_code = 405
            return response
        if user == 406:
            response = make_response(jsonify("Incorrect user data, try again"))
            response.status_code = 405
            return response
        response = make_response(jsonify(CreateUser().dump(user)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/user', methods=['GET'])
@auth.login_required
@admin_required
def get_all_users():
    try:
        users = db_utils.get_entry(User)
        response = make_response(jsonify(GetUser(many=True).dump(users)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/user/<int:id>', methods=['GET'])
@auth.login_required
@admin_required
def get_user(id: int):
    try:
        user = db_utils.get_entry_by_id(User, id)
        if user == 404:
            response = make_response(jsonify("Unknown user id"))
            response.status_code = 404
            return response
        response = make_response(jsonify(GetUser().dump(user)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/user/<int:id>', methods=['PUT'])
@auth.login_required
@admin_required
def update_user(id: int):
    try:
        user_data = GetUser().load(request.json)
        if len(user_data) == 0:
            response = make_response(jsonify("No data to change"))
            response.status_code = 405
            return response

        user = db_utils.get_entry_by_id(User, id)
        if user == 404:
            response = make_response(jsonify("Unknown user id"))
            response.status_code = 404
            return response
        if 'idlocation' in user_data and 'phone' in user_data and 'email' in user_data:
            new_user = db_utils.update_usr(id, phn=user_data['phone'], eml=user_data['email']
                                           , location=user_data['idlocation'], **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

        if 'idlocation' in user_data and 'phone' in user_data and 'email' not in user_data:
            new_user = db_utils.update_usr(id, phn=user_data['phone'], eml=None
                                           , location=user_data['idlocation'], **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

        if 'idlocation' in user_data and 'phone' not in user_data and 'email' in user_data:
            new_user = db_utils.update_usr(id, phn=None, eml=user_data['email']
                                           , location=user_data['idlocation'], **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

        if 'idlocation' in user_data and 'phone' not in user_data and 'email' not in user_data:
            new_user = db_utils.update_usr(id, phn=None, eml=None
                                           , location=user_data['idlocation'], **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

        if 'idlocation' not in user_data and 'phone' in user_data and 'email' in user_data:
            new_user = db_utils.update_usr(id, phn=user_data['phone'], eml=user_data['email']
                                           , location=None, **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

        if 'idlocation' not in user_data and 'phone' in user_data and 'email' not in user_data:
            new_user = db_utils.update_usr(id, phn=user_data['phone'], eml=None
                                           , location=None, **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

        if 'idlocation' not in user_data and 'phone' not in user_data and 'email' in user_data:
            new_user = db_utils.update_usr(id, phn=None, eml=user_data['email']
                                           , location=None, **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

        if 'idlocation' not in user_data and 'phone' not in user_data and 'email' not in user_data:
            new_user = db_utils.update_usr(id, phn=None, eml=None
                                           , location=None, **user_data)
            if new_user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if new_user == 405:
                response = make_response(jsonify("Not correct values entered"))
                return response
            if new_user == 406:
                response = make_response(jsonify("Duplicate value entered"))
                return response
            response = make_response(jsonify(GetUser().dump(new_user)))
            response.status_code = 200
            return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/user/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_user(id: int):
    try:
        user = db_utils.delete_entry_by_id(User, id)
        print(user)
        if user == 404:
            response = make_response(jsonify("Unknown user id"))
            response.status_code = 404
            return response
        response = make_response(jsonify(f"Successfully delete {id}"))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route("/user/self", methods=["GET", "DELETE", "PUT"])
@auth.login_required
def user_self():
    email = auth.current_user()
    '''
    if not auth.current_user():
        print('ya eblan')
        response = make_response('You are not logged in')
        response.status_code = 410
        return response
    '''
    user = db_utils.get_entry_by_email(User, email)

    selfId = user.id

    if request.method == "GET":
        user = db_utils.get_entry_by_id(User, selfId)
        response = make_response(jsonify(UserData().dump(user)), 200)
        return response

    if request.method == "DELETE":
        user = db_utils.delete_entry_by_id(User, selfId)
        response = make_response('Success', 200)
        return response

    if request.method == "PUT":
        try:
            user_data = GetUser().load(request.json)
            if len(user_data) == 0:
                response = make_response(jsonify("No data to change"))
                response.status_code = 405
                return response

            user = db_utils.get_entry_by_id(User, selfId)
            if user == 404:
                response = make_response(jsonify("Unknown user id"))
                response.status_code = 404
                return response
            if 'idlocation' in user_data and 'phone' in user_data and 'email' in user_data:
                new_user = db_utils.update_usr(selfId, phn=user_data['phone'], eml=user_data['email']
                                               , location=user_data['idlocation'], **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

            if 'idlocation' in user_data and 'phone' in user_data and 'email' not in user_data:
                new_user = db_utils.update_usr(selfId, phn=user_data['phone'], eml=None
                                               , location=user_data['idlocation'], **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

            if 'idlocation' in user_data and 'phone' not in user_data and 'email' in user_data:
                new_user = db_utils.update_usr(selfId, phn=None, eml=user_data['email']
                                               , location=user_data['idlocation'], **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

            if 'idlocation' in user_data and 'phone' not in user_data and 'email' not in user_data:
                new_user = db_utils.update_usr(selfId, phn=None, eml=None
                                               , location=user_data['idlocation'], **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

            if 'idlocation' not in user_data and 'phone' in user_data and 'email' in user_data:
                new_user = db_utils.update_usr(selfId, phn=user_data['phone'], eml=user_data['email']
                                               , location=None, **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

            if 'idlocation' not in user_data and 'phone' in user_data and 'email' not in user_data:
                new_user = db_utils.update_usr(selfId, phn=user_data['phone'], eml=None
                                               , location=None, **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

            if 'idlocation' not in user_data and 'phone' not in user_data and 'email' in user_data:
                new_user = db_utils.update_usr(selfId, phn=None, eml=user_data['email']
                                               , location=None, **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

            if 'idlocation' not in user_data and 'phone' not in user_data and 'email' not in user_data:
                new_user = db_utils.update_usr(selfId, phn=None, eml=None
                                               , location=None, **user_data)
                if new_user == 404:
                    response = make_response(jsonify("Unknown user id"))
                    response.status_code = 404
                    return response
                if new_user == 405:
                    response = make_response(jsonify("Not correct values entered"))
                    return response
                if new_user == 406:
                    response = make_response(jsonify("Duplicate value entered"))
                    return response
                response = make_response(jsonify(GetUser().dump(new_user)))
                response.status_code = 200
                return response

        except ValidationError as err:
            response = dict({"Uncorrect fields": err.normalized_messages()})
            return response, 400


@api_blueprint.route('/advertisement/local', methods=['POST'])
@auth.login_required
def create_local_ad():
    try:
        localad_data = CreateLocalAd().load(request.json)
        if 'title' not in localad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        if 'id_category' not in localad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        if 'status' not in localad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        if 'publishingDate' not in localad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        # if 'user_id' not in localad_data:
        # response = make_response(jsonify("Missing required fields"))
        # response.status_code = 405
        # return response
        if 'location_id' not in localad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        email = auth.current_user()
        user = db_utils.get_entry_by_email(User, email)
        selfId = user.id
        localad_data['user_id'] = selfId
        localdad = db_utils.create_localad(category=localad_data['id_category'], user=selfId,
                                           location=localad_data['location_id'], **localad_data)
        if localdad == 405:
            response = make_response(jsonify("Incorrect data"))
            response.status_code = 405
            return response
        response = make_response(jsonify(CreateLocalAd().dump(localdad)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/local', methods=['GET'])
@auth.login_required
def get_local_ad():
    email = auth.current_user()
    user = db_utils.get_entry_by_email(User, email)
    locId = user.idlocation
    try:
        ad = db_utils.get_local_ad_by_location(LocalAd, locId)
        response = make_response(jsonify(GetLocalAd(many=True).dump(ad)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/local/<int:id>', methods=['GET'])
@auth.login_required
def get_local_ad_(id: int):
    try:
        ad = db_utils.get_entry_by_id(LocalAd, id)
        if ad == 404:
            response = make_response(jsonify("Unknown local ad id"))
            response.status_code = 404
            return response
        response = make_response(jsonify(GetLocalAd().dump(ad)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/local/<int:id>', methods=['PUT'])
@auth.login_required
def update_local_ad(id: int):
    getLocalData = db_utils.get_entry_by_id(LocalAd, id)
    email = auth.current_user()
    user = db_utils.get_entry_by_email(User, email)
    selfId = user.id
    try:
        localad_data = GetLocalAd().load(request.json)
        if len(localad_data) == 0:
            response = make_response(jsonify("No data to change"))
            response.status_code = 405
            return response


        localad = db_utils.get_entry_by_id(LocalAd, id)
        if localad == 404:
            respose = make_response(jsonify("Unknown user id"))
            respose.status_code = 404
            return respose
        if getLocalData.user_id != selfId:
            response = make_response('Error: you can`t update someones ad')
            response.status_code = 407
            return response
        if 'id_category' in localad_data and 'location_id' in localad_data:
            new_localad = db_utils.update_localad(id, category=localad_data['id_category'],
                                                  user=selfId
                                                  , location=localad_data['location_id'], **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        if 'id_category' in localad_data and 'location_id' not in localad_data:
            new_localad = db_utils.update_localad(id, category=localad_data['id_category'],
                                                  user=selfId
                                                  , location=None, **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        '''
        if 'id_category' in localad_data and 'user_id' not in localad_data and 'idlocation' in localad_data:
            new_localad = db_utils.update_localad(id, category=localad_data['id_category'],
                                                  user=None
                                                  , location=localad_data['idlocation'], **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        if 'id_category' in localad_data and 'user_id' not in localad_data and 'idlocation' not in localad_data:
            new_localad = db_utils.update_localad(id, category=localad_data['id_category'],
                                                  user=None
                                                  , location=None, **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        '''
        if 'id_category' not in localad_data and 'location_id' in localad_data:
            new_localad = db_utils.update_localad(id, category=None,
                                                  user=selfId
                                                  , location=localad_data['location_id'], **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        if 'id_category' not in localad_data and 'location_id' not in localad_data:
            new_localad = db_utils.update_localad(id, category=None,
                                                  user=selfId
                                                  , location=None, **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        '''
        if 'id_category' not in localad_data and 'user_id' not in localad_data and 'idlocation' in localad_data:
            new_localad = db_utils.update_localad(id, category=None,
                                                  user=None
                                                  , location=['idlocation'], **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        if 'id_category' not in localad_data and 'user_id' not in localad_data and 'idlocation' not in localad_data:
            new_localad = db_utils.update_localad(id, category=None,
                                                  user=None
                                                  , location=None, **localad_data)
            if new_localad == 400:
                respose = make_response(jsonify("Unknown user id"))
                respose.status_code = 404
                return respose
            if new_localad == 405:
                respose = make_response(jsonify("Not correct values entered"))
                respose.status_code = 405
                return respose
            response = make_response(jsonify(GetLocalAd().dump(new_localad)))
            response.status_code = 200
            return response
        '''
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/local/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_local_ad(id: int):
    try:
        email = auth.current_user()
        user = db_utils.get_entry_by_email(User, email)
        selfId = user.id
        getLocalAd = db_utils.get_entry_by_id(LocalAd, id)
        if getLocalAd == 404:
            response = make_response(jsonify("Unknown local ad id"))
            response.status_code = 404
            return response
        if getLocalAd.user_id != selfId:
            response = make_response('Error: you can`t delete someones ad')
            response.status_code = 407
            return response
        localad = db_utils.delete_entry_by_id(LocalAd, id)
        if localad == 404:
            response = make_response(jsonify("Unknown local ad id"))
            response.status_code = 404
            return response

        response = make_response(jsonify(f"Successfully delete {id}"))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/public', methods=['POST'])
@auth.login_required
def create_public_ad():
    try:
        publicad_data = CreatePublicAd().load(request.json)
        if 'title' not in publicad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        if 'id_category' not in publicad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        if 'status' not in publicad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        if 'publishingDate' not in publicad_data:
            response = make_response(jsonify("Missing required fields"))
            response.status_code = 405
            return response
        # if 'user_id' not in publicad_data:
        # response = make_response(jsonify("Missing required fields"))
        # response.status_code = 405
        # return response
        email = auth.current_user()
        user = db_utils.get_entry_by_email(User, email)
        selfId = user.id
        publicad_data['user_id'] = selfId
        publicad = db_utils.create_publicad(category=publicad_data['id_category'], user=selfId,
                                            **publicad_data)
        if publicad == 405:
            response = make_response(jsonify("Incorrect data"))
            response.status_code = 405
            return response
        response = make_response(jsonify(CreatePublicAd().dump(publicad)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/public', methods=['GET'])
def get_public_ad():
    try:
        publicad = db_utils.get_entry(PublicAd)
        response = make_response(jsonify(GetPublicAd(many=True).dump(publicad)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/public/<int:id>', methods=['GET'])
def get_public_ad_(id: int):
    try:
        ad = db_utils.get_entry_by_id(PublicAd, id)
        if ad == 404:
            response = make_response(jsonify("Unknown public ad id"))
            response.status_code = 404
            return response
        response = make_response(jsonify(GetPublicAd().dump(ad)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/public/<int:id>', methods=['PUT'])
@auth.login_required
def update_public_ad(id: int):
    getPublicData = db_utils.get_entry_by_id(PublicAd, id)
    email = auth.current_user()
    user = db_utils.get_entry_by_email(User, email)
    selfId = user.id
    try:


        publicad_data = GetPublicAd().load(request.json)
        if len(publicad_data) == 0:
            response = make_response(jsonify("No data to change"))
            response.status_code = 405
            return response

        publicad = db_utils.get_entry_by_id(PublicAd, id)
        if publicad == 404:
            response = make_response(jsonify("Unknown public ad id"))
            response.status_code = 404
            return response
        if getPublicData.user_id != selfId:
            response = make_response('Error: you can`t update someones ad')
            response.status_code = 407
            return response
        if 'id_category' in publicad_data:
            new_publicad = db_utils.update_publicad(id, category=publicad_data['id_category'],
                                                    user=selfId, **publicad_data)
            if new_publicad == 404:
                response = make_response(jsonify("Unknown public ad id"))
                response.status_code = 404
                return response
            if new_publicad == 405:
                response = make_response(jsonify("Not correct values entered"))
                response.status_code = 405
                return response

            response = make_response(jsonify(GetPublicAd().dump(new_publicad)))
            response.status_code = 200
            return response

        if 'user_id' in publicad_data:
            response = make_response('You can`t update user field')
            response.status_code = 410
            return response
        '''
        if 'id_category' in publicad_data and 'user_id' not in publicad_data:
            new_publicad = db_utils.update_publicad(id, category=publicad_data['id_category'],
                                                    user=None, **publicad_data)
            if new_publicad == 404:
                response = make_response(jsonify("Unknown public ad id"))
                response.status_code = 404
                return response
            if new_publicad == 405:
                response = make_response(jsonify("Not correct values entered"))
                response.status_code = 405
                return response

            response = make_response(jsonify(GetPublicAd().dump(new_publicad)))
            response.status_code = 200
            return response
        if 'id_category' not in publicad_data and 'user_id' in publicad_data:
            new_publicad = db_utils.update_publicad(id, category=None,
                                                    user=publicad_data['user_id'], **publicad_data)
            if new_publicad == 404:
                response = make_response(jsonify("Unknown public ad id"))
                response.status_code = 404
                return response
            if new_publicad == 405:
                response = make_response(jsonify("Not correct values entered"))
                response.status_code = 405
                return response

            response = make_response(jsonify(GetPublicAd().dump(new_publicad)))
            response.status_code = 200
            return response
        '''
        if 'id_category' not in publicad_data:
            new_publicad = db_utils.update_publicad(id, category=None,
                                                    user=selfId, **publicad_data)
            if new_publicad == 404:
                response = make_response(jsonify("Unknown public ad id"))
                response.status_code = 404
                return response
            if new_publicad == 405:
                response = make_response(jsonify("Not correct values entered"))
                response.status_code = 405
                return response

            response = make_response(jsonify(GetPublicAd().dump(new_publicad)))
            response.status_code = 200
            return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


@api_blueprint.route('/advertisement/public/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_public_ad(id: int):
    try:
        email = auth.current_user()
        user = db_utils.get_entry_by_email(User, email)
        selfId = user.id
        getPublicAd = db_utils.get_entry_by_id(PublicAd, id)
        if getPublicAd == 404:
            response = make_response(jsonify("Unknown local ad id"))
            response.status_code = 404
            return response
        if getPublicAd.user_id != selfId:
            response = make_response('Error: you can`t delete someones ad')
            response.status_code = 407
            return response
        publicad = db_utils.delete_entry_by_id(PublicAd, id)
        if publicad == 404:
            response = make_response(jsonify("Unknown public ad id"))
            response.status_code = 404
            return response

        response = make_response(jsonify(f"Successfully delete {id}"))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400


'''
@api_blueprint.route('/user/logout', methods=['GET'])
def logout():
    return "Log out page"
'''

"""
{
    "firstName": "FirstUser1Name",
    "lastName": "LastUser1Name",
    "email": "user1@localhost.com",
    "password": "123qwe123",
    "phone": "0987564321",
    "userStatus": "premium",
    "idlocation": 1,
    "isAdmin":1
}
{
    "title": "LocalAd1",
    "id_category": 1,
    "status": "active",
    "publishingDate": "2022-05-01 23:05:21",
    "user_id": 1,
    "location_id": 1
}
{
    "title": "PublicAd1",
    "id_category": 1,
    "status": "active",
    "publishingDate": "2022-05-01 23:05:21",
    "user_id": 1
}
"""
