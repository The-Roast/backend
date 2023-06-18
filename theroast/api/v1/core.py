from flask import Blueprint, request, jsonify
from ...db.schemas import *

core = Blueprint('core', __name__, url_prefix = "/v1")

@core.route("/digest/<uuid>", methods = ['GET'])
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
def set_digest():

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
    db.session.add(digest)
    from .auth import current_user
    current_user.digests.append(digest)
    db.session.add(current_user)
    db.session.commit()

    return {
        "message": "Created digest.",
        "status": 200
    }

@core.route("/user/<email>", methods = ['GET'])
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
def get_current_user():

    from .auth import current_user

    return current_user.as_dict()