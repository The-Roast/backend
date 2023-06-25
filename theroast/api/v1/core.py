import json
from flask import Blueprint, request, jsonify
from theroast.theroast.data.news import SOURCES
from theroast.theroast.lib.models import run_openai
from ...db.schemas import Users, Digests
from ...extensions import db

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

    from .auth import current_user
    assert current_user[0]

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

        user = Users.query.filter_by(id = current_user[0]).first()
        db.session.add(digest)
        user.digests.append(digest)
        db.session.commit()

        return {
            "message": "Created digest.",
            "status": 200
        }
    
    elif len(request.json["uuid"]) > 0:

        digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

        if not digest:
            return {
                "message": "Invalid uuid given.",
                "status": 404
            }

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

        return {
            "message": "Updated digest.",
            "status": 200
        }
    
    else:

        user: Users = Users.query.filter_by(id = current_user[0]).first()
        digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

        if not digest:
            return {
                "message": "Invalid uuid given.",
                "status": 404
            }

        user.digests.remove(digest)

        db.session.commit()

        return {
            "message": "Deleted digest.",
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

    assert current_user[0]

    user: Users = Users.query.filter_by(id = current_user[0]).first()

    return user.as_dict()

@core.route("/newsletter/<uuid>", methods = ['GET'])
def get_newsletter(uuid):

    from .auth import current_user

    assert current_user[0]

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    
    if not digest:
        return jsonify({
            "message": "No newsletter exists",
            "status": 404
        })
    
    sects, coll, current_user[1] = run_openai(
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

# @core.route("/chat", methods = ["GET"])