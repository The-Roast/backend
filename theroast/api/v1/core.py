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
        return {
            "response": {"message": "Digest not found."},
            "ok": False
         }, 404

    return {
        "response": digest.as_dict(),
        "ok": True
    }, 200

@core.route("/digest", methods = ['POST'])
@jwt_required()
def set_digest():

    id = get_jwt_identity()
    current_user = Users.query.filter_by(id = id).first()

    if request.json["uuid"] == "":

        name = request.json["name"]
        settings = {
            "sources": request.json["sources"],
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

        return {
            "response": {"uuid": str(digest.uuid)},
            "ok": True
        }, 200
    
    elif len(request.json["uuid"]) > 0:

        digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

        if not digest:
            return {
                "response": {"message": "Invalid uuid given."},
                "ok": False
            }, 404

        settings = {
            "sources": request.json["sources"],
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

        return {
            "response": {"uuid": str(digest.uuid)},
            "ok": True
        }, 200
    
    else:

        digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

        if not digest:
            return {
                "response": {"message": "Invalid uuid given."},
                "ok": False
            }, 404

        current_user.digests.remove(digest)

        db.session.commit()

        return {
            "response": {"message": "Deleted digest."},
            "ok": True
        }, 200

@core.route("/user/<id>", methods = ['GET'])
@jwt_required()
def get_user(id):

    user: Users = Users.query.filter_by(id = id).first()
    if not user:
        return {
            "response": {"message": "User not found."},
            "ok": False
        }, 404

    response = user.as_dict()
    response["digests"] = [d.as_dict() for d in user.digests]

    return {
        "response": response,
        "ok": True
    }, 200

@core.route("/user", methods = ['GET'])
@jwt_required()
def get_current_user():

    id = get_jwt_identity()

    return {
        "response": {"id": id},
        "ok": True
    }, 200

@core.route("/newsletter/<uuid>", methods = ['GET'])
@jwt_required()
def get_newsletter(uuid):

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    
    if not digest:
        return {
            "response": {"message": "No newsletter exists"},
            "ok": False
        }, 404
    
    sects, coll, _ = run_openai(
        list(digest.settings["interests"]),
        list(digest.settings["sources"]),
        digest.settings["personality"]
    )
    response = coll
    for sect in sects:
        response[sect["title"]] = sect["body"]

    return {
        "response": response,
        "ok": True
    }, 200

@core.route("/chat", methods = ["GET"])
@jwt_required()
def chat():

    return {
        "response": {"message": "This is dummy text."},
        "ok": True
    }, 200