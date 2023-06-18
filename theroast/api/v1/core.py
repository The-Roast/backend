from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...db.schemas import *

core = Blueprint('core', __name__, url_prefix = "/v1")

@core.route("/digest/<uuid>", methods = ['GET'])
@jwt_required()
def get_digest(uuid):

    assert uuid and isinstance(uuid, str)

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    if not digest:
        return {
            "message": "Digest not found.",
            "status": 404
        }

    return digest.as_dict()

@core.route("/digest", methods = ['POST'])
@jwt_required()
def set_digest():

    id = get_jwt_identity()

    name = request.json["name"]
    settings = {
        "sources": request.json["contentSources"],
        "interests": request.json["interests"],
        "personality": request.json["personality"]
    }
    color = request.json["color"]["hex"]
    digest = Digests(
        name = name,
        settings = settings,
        color = color
    )
    user = Users.query.filter_by(id = id).first()
    db.session.add(digest)
    user.digests.append(digest)
    db.session.commit()

    return {
        "message": "Created digest.",
        "status": 200
    }

@core.route("/user/<email>", methods = ['GET'])
@jwt_required()
def get_user(email):

    assert email and isinstance(email, str)
    
    user: Users = Users.query.filter_by(email = email).first()
    if not user:
        return {
            "message": "User not found.",
            "status": 404
        }
    response = user.as_dict()
    response["digests"] = [d.as_dict() for d in user.digests]

    return response

@core.route("/user", methods = ['GET'])
@jwt_required()
def get_current_user():

    id = get_jwt_identity()

    user: Users = Users.query.filter_by(id = id).first()

    return user.as_dict()