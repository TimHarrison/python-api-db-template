from flask import request, jsonify
from lib.model.users import User
from flask.helpers import url_for
from application import app
from lib.model import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from lib.model.organization import Organization
from lib.exceptions.organization import InvalidCreateOrganizationPayload,\
    OrganizationExists, AlreadyOwnOrg, NoOrganizationFound,\
    DontBelongToOrganization

jwt = JWTManager(app)

@app.route('/api/organization', methods = ['POST'])
@jwt_required
def new_organization():
    user = User().query.filter_by(username = get_jwt_identity()).first()
    #===========================================================================
    # Fetch data from json payload
    #===========================================================================
    request.get_data()  # @UndefinedVariable
    name = request.json.get('name', None)  # @UndefinedVariable
    description = request.json.get('description', None)  # @UndefinedVariable
    admin_id = user.get_id()
    active = False
    
    #===========================================================================
    # Rules
    #===========================================================================
    # User's can only own one organization for now
    if Organization().query.filter_by(admin_id = admin_id).first() is not None:
        raise AlreadyOwnOrg()
    # Organization must have a name passed with the payload
    if not name:
        raise InvalidCreateOrganizationPayload(request.json)  # @UndefinedVariable
    # Organization name must be unique
    if Organization().query.filter_by(name = name).first() is not None:
        raise OrganizationExists()
     
    #===========================================================================
    # Create object
    #===========================================================================
    org = Organization(name = name)
    org.set_description(description)
    org.set_admin_id(admin_id)
    org.set_active(active)
     
    #===========================================================================
    # Commit to the database
    #===========================================================================
    failed = False
    try:
        db.session.add(org)  # @UndefinedVariable
        db.session.commit()  # @UndefinedVariable
    except Exception as e:
        db.session.rollback()  # @UndefinedVariable
        db.session.flush()  # @UndefinedVariable
        failed = True
    
    #===========================================================================
    # Update user with new organization id
    #===========================================================================
    if not failed:
        user.set_organization_id(org.id)
        db.session.add(user)  # @UndefinedVariable
        db.session.commit()  # @UndefinedVariable
     
    #===========================================================================
    # Respond with properly formatted json object
    #===========================================================================
    print(org.to_dict())
    return jsonify(org.to_dict()), 201, {'Location': url_for('new_organization', id = org.id, _external = True)}


@app.route('/api/organization', methods = ['GET'])
@jwt_required
def get_organization():
    user_id = User().query.filter_by(username = get_jwt_identity()).first().get_id()
    org = Organization().query.filter_by(admin_id = user_id).first()
    if org is None:
        raise NoOrganizationFound() 
    return jsonify(org.to_dict()), 200



@app.errorhandler(OrganizationExists)
def handle_organization_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(AlreadyOwnOrg)
def handle_already_own_org(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(NoOrganizationFound)
def handle_no_organization_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(InvalidCreateOrganizationPayload)
def handle_invalid_organization_create_payload(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response