import json
from flask import Blueprint, request, jsonify
from theroast.theroast.data.news import SOURCES
from theroast.theroast.lib.models import generate_newsletter, get_news, parse_markdown
from ...db.schemas import Users, Digests, Newsletters
from ...extensions import db, mail
from flask_jwt_extended import jwt_required, get_jwt_identity
from textwrap import dedent

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

    uuid = get_jwt_identity()
    current_user = Users.query.filter_by(uuid = uuid).first()

    name = request.json["name"]
    settings = {
        "sources": [SOURCES[s.lower().strip()] for s in request.json["sources"].split(",") if s.lower().strip() in SOURCES.keys()],
        "interests": [i.lower().strip() for i in request.json["interests"].split(",")],
        "personality": request.json["personality"]
    }
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

@core.route("/digest/<uuid>", methods = ['PUT'])
@jwt_required()
def update_digest(uuid):

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()

    if not digest:
        return {
            "response": {"message": "Invalid uuid given."},
            "ok": False
        }, 404

    digest.settings = {
        "sources": [SOURCES[s.lower().strip()] for s in request.json["sources"].split(",") if s.lower().strip() in SOURCES.keys()],
        "interests": [i.lower().strip() for i in request.json["interests"].split(",")],
        "personality": request.json["personality"]
    }
    digest.name = request.json["name"]
    digest.color = request.json["color"]["hex"]

    db.session.commit()

    return {
        "response": {"uuid": str(digest.uuid)},
        "ok": True
    }, 200

@core.route("/digest", methods = ['DELETE'])
@jwt_required()
def delete_digest():

    uuid = get_jwt_identity()
    current_user = Users.query.filter_by(uuid = uuid).first()

    digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

    if not digest:
        return {
            "response": {"message": "Invalid uuid given."},
            "ok": False
        }, 404

    current_user.digests.remove(digest)
    db.session.delete(digest)

    db.session.commit()

    return {
        "response": {"message": "Deleted digest."},
        "ok": True
    }, 200

@core.route("/user", methods = ['GET'])
@jwt_required()
def get_current_user():

    uuid = get_jwt_identity()

    return {
        "response": {"uuid": uuid},
        "ok": True
    }, 200

@core.route("/user/<uuid>", methods = ['GET'])
@jwt_required()
def get_user(uuid):

    user: Users = Users.query.filter_by(uuid = uuid).first()
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

@core.route("/user", methods = ['PUT'])
@jwt_required()
def update_user():

    uuid = get_jwt_identity()
    current_user: Users = Users.query.filter_by(uuid = uuid).first()

    email = request.json["email"] # Not viable in future as need to check
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    old_password = request.json["old_password"]
    new_password = request.json["new_password"] # Not viable in future as need to check

    if old_password and not current_user.check_password(old_password):
        return {
            "response": {"message": "Incorrect password is not valid."},
            "ok": True
        }, 403

    elif old_password and current_user.check_password(old_password):
        current_user.password = new_password
        current_user.hash_password()

    current_user.email = email if email else current_user.email
    current_user.first_name = first_name if first_name else current_user.first_name
    current_user.last_name = last_name if last_name else current_user.last_name

    db.session.commit()

    return {
        "response": {"uuid": str(current_user.uuid)},
        "ok": True
    }, 200

@core.route("/user", methods = ['DELETE'])
@jwt_required()
def delete_user():

    uuid = get_jwt_identity()
    current_user: Users = Users.query.filter_by(uuid = uuid).first()
    db.session.delete(current_user)

    db.session.commit()

    return {
        "response": {"message": "Deleted user"},
        "ok": True
    }, 200

# Get Newsletters by Digest -> "GET /digest/<uuid>/newsletters" -> Stipulation argument within digest
# Create Newsletter By Digest -> "GET /digest/<uuid>/create"
# Update Newsletter By Digest ->  "PUT /digest/<digest_uuid>/newsletter/<newsletter_uuid>"
# Get Newsletter By UUID -> "GET /newsletter/<uuid>"
# Delete Newsletter By UUID -> "DELETE /newsletter/<uuid>"

@core.route("/digest/<uuid>/newsletters", methods = ['GET'])
@jwt_required()
def get_digest_history(uuid):

    digest: Digests = Digests.query.filter_by(uuid = uuid).first() 
    if not digest:
        return {
            "response": {"message": "Digest not found"},
            "ok": False
        }, 404
    newsletters = [n.as_dict() for n in sorted(digest.newsletters, lambda x: x.created_at)]

    return {
        "response": {
            "newsletters": newsletters,
            "digest_uuid": uuid
        },
        "ok": True
    }, 200

@core.route("/digest/<uuid>/create")
@jwt_required()
def create_newsletter(uuid):

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    
    if not digest:
        return {
            "response": {"message": "Digest not found."},
            "ok": False
        }, 404
    
    interests = digest.settings["interests"]
    sources = digest.settings["sources"]
    personality = digest.settings["personality"]

    articles = get_news(interests, sources)
    sections, structure = generate_newsletter(articles, interests, personality)
    
    data = structure
    data["sections"] = sections

    #add newsletters tie to articles
    newsletter = Newsletters(
        data = data,
        digest = digest
    )
    db.session.add(newsletter)
    db.session.commit()

    return {
        "response": {"uuid": newsletter.uuid},
        "ok": True
    }, 200



@core.route("/digest/<digest_uuid>/newsletter/<newsletter_uuid>", methods = ['PUT'])
def regenerate_newsletter(digest_uuid, newsletter_uuid):

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    
    if not digest:
        return {
            "response": {"message": "Digest not found."},
            "ok": False
        }, 404


@core.route("/newsletter/<uuid>", methods = ['GET'])
@jwt_required()
def get_newsletter(uuid):

    newsletter: Newsletters = Newsletters.query.filter_by(uuid = uuid).first()
    if not newsletter:
        return {
            "response": {"message": "Newsletter not found."},
            "ok": False
        }, 404
    newsletter.clicks += 1

    return {
        "response": newsletter.as_dict(exclude_data = False),
        "ok": True
    }, 200

@core.route("/newsletter/<uuid>", methods = ['DELETE'])
def delete_newsletter(uuid):

    newsletter: Newsletters = Newsletters.query.filter_by(uuid = uuid).first()
    if not newsletter:
        return {
            "response": {"message": "Newsletter not found."},
            "ok": False
        }, 404

    db.session.delete(newsletter)
    db.session.commit()

@core.route("/chat", methods = ["GET"])
@jwt_required()
def chat():

    return {
        "response": {"message": "This is dummy text."},
        "ok": True
    }, 200
