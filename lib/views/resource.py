from flask import request, jsonify
from lib.model.users import User
from flask.helpers import url_for
from application import app
from lib.model import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from lib.model.organization import Organization
from lib.exceptions.organization import NoOrganizationFound,\
    DontBelongToOrganization, OrganizationNotVerified
from lib.model.resource import Resource
from lib.exceptions.resource import InvalidCreateResourcePayload

jwt = JWTManager(app)

@app.route('/api/resource', methods = ['POST'])
@jwt_required
def new_resource():
    user = User().query.filter_by(username = get_jwt_identity()).first()
    #===========================================================================
    # Fetch data from json payload
    #===========================================================================
    request.get_data()  # @UndefinedVariable
    name = request.json.get('name', None)  # @UndefinedVariable
    owner_id = user.get_id()
    organization_id = request.json.get('organization_id', None)  # @UndefinedVariable
    resource_type = request.json.get('resource_type', None)  # @UndefinedVariable
    publish_status = request.json.get('publish_status', 'draft')  # @UndefinedVariable
    description = request.json.get('description', None)  # @UndefinedVariable
    featured_image = request.json.get('featured_image', None)  # @UndefinedVariable
    publish_date = db.Column(db.DateTime(timezone=True))  # @UndefinedVariable
    
    #===========================================================================
    # Rules
    #===========================================================================
    # Owner must belong to the organization
    if int(user.get_organization_id()) != int(organization_id):
        raise DontBelongToOrganization(organization_id)
    # Organization must be verified
    if Organization().query.filter_by(id = organization_id).first().get_verified() is False:
        raise OrganizationNotVerified("creating a resource")
    # If publish_status is not set, set to 'draft'
    if publish_status is None:
        publish_status = 'draft'
    # Fields must be set
    if name is None or organization_id is None or resource_type is None:
        raise InvalidCreateResourcePayload(request.json)  # @UndefinedVariable
     
    #===========================================================================
    # Create object
    #===========================================================================
    resource = Resource(name = name)
    resource.set_description(description)
    resource.set_owner_id(owner_id)
    resource.set_organization_id(organization_id)
    resource.set_resource_type(resource_type)
    resource.set_publish_status(publish_status)
    resource.set_featured_image(featured_image)
    resource.set_publish_date(publish_date)
     
    #===========================================================================
    # Commit to the database
    #===========================================================================
    db.session.add(resource)  # @UndefinedVariable
    db.session.commit()  # @UndefinedVariable
     
    #===========================================================================
    # Respond with properly formatted json object
    #===========================================================================
    print(resource.to_dict())
    return jsonify(resource.to_dict()), 201, {'Location': url_for('new_resource', id = resource.id, _external = True)}


@app.route('/api/resource', methods = ['GET'])
@jwt_required
def get_resource():
    user_id = User().query.filter_by(username = get_jwt_identity()).first().get_id()
    org = Organization().query.filter_by(admin_id = user_id).first()
    if org is None:
        raise NoOrganizationFound() 
    return jsonify(org.to_dict()), 200



@app.errorhandler(DontBelongToOrganization)
def handle_dont_belong_organization(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(OrganizationNotVerified)
def handle_organization_not_verified(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(InvalidCreateResourcePayload)
def handle_invalid_create_resource_payload(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response