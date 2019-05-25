from flask import request, jsonify
from lib.model.users import User
from flask.helpers import url_for
from lib.exceptions.Authentication import UserExists, UserLoginFailed, InvalidCreateUserPayload,\
    InvalidUserType
from application import app
from lib.model import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, create_refresh_token, jwt_refresh_token_required
from lib.payloads.session_response import SessionResponse
from lib.util.constants import UserRolesEnum

jwt = JWTManager(app)

@app.route('/api/signup', methods = ['POST'])
def new_user():
    request.get_data()  # @UndefinedVariable
    username = request.json.get('username', None)  # @UndefinedVariable
    password = request.json.get('password', None)  # @UndefinedVariable
    email = request.json.get('email', None)  # @UndefinedVariable
    name = request.json.get('name', None)  # @UndefinedVariable
#     user_type = request.json.get('user_type', None)  # @UndefinedVariable
    if not username or not password or not email:
        raise InvalidCreateUserPayload(request.json)  # @UndefinedVariable
    if User().query.filter_by(username = username).first() is not None:
        raise UserExists()
    user = User(username = username)
    user.set_password(user.hash_password(password))
    user.set_email(email)
    user.set_full_name(name)
#     if user_type not in UserRolesEnum.ALL_ROLES:
#         raise InvalidUserType(request.json)  # @UndefinedVariable
    user.set_role_id('user')
    db.session.add(user)  # @UndefinedVariable
    db.session.commit()  # @UndefinedVariable
    return jsonify(SessionResponse(user.to_dict(), user.get_organization_id(), create_access_token(identity=username), create_refresh_token(identity=username)).to_dict()), 201, {'Location': url_for('new_user', id = user.id, _external = True)}


@app.route('/api/login', methods = ['POST'])
def login():
    request.get_data()  # @UndefinedVariable
    email = request.json['email']  # @UndefinedVariable
    password = request.json['password']  # @UndefinedVariable
    if email is None or password is None:
        raise UserLoginFailed(request.json)  # @UndefinedVariable
    user = User().query.filter_by(email = email).first()
    if user is None:
        raise UserLoginFailed()
    else:
        if user.verify_password(password):
            access_token = create_access_token(identity=user.get_username(), fresh=True)
            refresh_token = create_refresh_token(user.get_username(), False)
            return jsonify(SessionResponse(user.to_dict(), user.get_organization_id(), access_token, refresh_token).to_dict()), 200, {"Authorization": "Bearer %s" % access_token}
        else:
            raise UserLoginFailed()


@app.route('/api/refresh_token', methods = ['POST'])
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    return jsonify(SessionResponse(None, create_access_token(identity=current_user), create_refresh_token(identity=current_user)).to_dict()), 200


@app.route('/api/user', methods = ['GET'])
@jwt_required
def get_user_info():
    current_user = get_jwt_identity()
    user = User().query.filter_by(username = current_user).first()
    return jsonify(user.to_dict()), 200


@app.errorhandler(UserExists)
def handle_user_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(UserLoginFailed)
def handle_user_login_failed(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(InvalidCreateUserPayload)
def handle_invalid_user_create_payload(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(InvalidUserType)
def handle_invalid_user_type(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response