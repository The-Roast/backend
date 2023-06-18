from flask import Blueprint, request, jsonify
from ...db.schemas import *

core = Blueprint('core', __name__, url_prefix = "/v1")

@core.route("/digest/<uuid>", methods = ['GET'])
def get_digest(uuid):

    assert uuid and isinstance(uuid, str)

    digest: Digests = Digests.objects.filter_by(uuid = uuid)
    if not digest:
        return {
            "message": "Digest not found.",
            "status": 404
        }

    return digest.as_dict()

@core.route("/digest", methods = ['POST'])
def set_digest():

    name = request.json["digestName"]
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

@core.route("/user/<email>", methods = ['GET'])
def get_user(email):

    assert email and isinstance(email, str)

    user: Users = Users.objects.filter_by(email = email)
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