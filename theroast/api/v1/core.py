import json
from flask import Blueprint, request, jsonify
from theroast.theroast.data.news import SOURCES
from theroast.theroast.lib.models import run_openai
from ...db.schemas import Users, Digests
from ...extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

core = Blueprint('core', __name__, url_prefix = "/v1")

@core.route("/digest/<uuid>", methods = ['GET'])
@jwt_required()
def get_digest(uuid):

    assert uuid and isinstance(uuid, str)

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    if not digest:
        return {"message": "Digest not found."}, 404

    return digest.as_dict(), 200

@core.route("/digest", methods = ['POST'])
@jwt_required()
def set_digest():

    id = get_jwt_identity()
    current_user = Users.query.filter_by(id = id).first()

    if request.json["uuid"] == "":

        name = request.json["name"]
        settings = {
            "sources": request.json["contentSources"],
            "interests": request.json["interests"],
            "personality": request.json["personality"]
        }
            
        for source in settings["sources"]:
            if source not in SOURCES:
                settings["sources"].remove(source)

        color = request.json["color"]["hex"]
        digest = Digests(
            name = name,
            settings = settings,
            color = color
        )

        db.session.add(digest)
        current_user.digests.append(digest)
        db.session.commit()

        return {"message": "Created digest."}, 200
    
    elif len(request.json["uuid"]) > 0:

        digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

        if not digest:
            return {"message": "Invalid uuid given."}, 404

        settings = {
            "sources": request.json["contentSources"],
            "interests": request.json["interests"],
            "personality": request.json["personality"]
        }
        for source in settings["sources"]:
            if source not in SOURCES:
                settings["sources"].remove(source)

        digest.name = request.json["name"]
        digest.color = request.json["color"]["hex"]
        digest.settings = settings

        db.session.commit()

        return {"message": "Updated digest."}, 200
    
    else:

        digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

        if not digest:
            return {"message": "Invalid uuid given."}, 404

        current_user.digests.remove(digest)

        db.session.commit()

        return {"message": "Deleted digest."}, 200

@core.route("/user/<id>", methods = ['GET'])
@jwt_required
def get_user(id):

    user: Users = Users.query.filter_by(id = id).first()
    if not user:
        return {"message": "User not found."}, 404

    response = user.as_dict()
    response["digests"] = [d.as_dict() for d in user.digests]

    return response

@core.route("/user", methods = ['GET'])
@jwt_required
def get_current_user():

    id = get_jwt_identity()

    return {"id": id}, 200

@core.route("/newsletter/<uuid>", methods = ['GET'])
@jwt_required
def get_newsletter(uuid):

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    
    if not digest:
        return jsonify({
            "message": "No newsletter exists",
            "status": 404
        })
    
    sects, coll, _ = run_openai(
        list(digest.settings["interests"]),
        list(digest.settings["sources"]),
        digest.settings["personality"]
    )
    response = coll
    for sect in sects:
        response[sect["title"]] = sect["body"]

    return jsonify({
        "response": response,
        "status": 200
    })

@core.route("/chat", methods = ["GET"])
def chat():

    # from .auth import current_user

    # assert current_user[0] and current_user[1]

    return {
        "message": "This is dummy text.",
        "status": 200
    }