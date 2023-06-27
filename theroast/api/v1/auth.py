from flask import Blueprint, request, redirect, url_for, jsonify, session
from ...extensions import db
from ...db.schemas import Digests, Users, create_color
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST'])
def login():

    email = request.json["email"]
    user: Users = Users.query.filter_by(email = email).first()
    if not user:
        return {"message": "Email is invalid."}, 404

    authorized = user.check_password(request.get_json["password"])
    if not authorized:
        return {"message": "Password is invalid"}, 401

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity = str(user.id), expires_delta = expires)
    refresh_token = create_refresh_token(identity = str(user.id), expires_delta = expires)

    return {"access_token": access_token, "refresh_token": refresh_token}, 200

@auth.route('/signup', methods = ['POST'])
def signup():

    email = request.json["email"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    digest_name = request.json["digest_name"]
    interests = request.json["interests"]
    sources = request.json["sources"]
    personality = request.json["personality"]

    user = Users.query.filter_by(email = email).first()

    if user:
        return {"message": "Use a different email."}, 405

    user = Users(
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
    )
    user.hash_password()
    digest = Digests(
        name = digest_name,
        settings = {
            "interests": interests,
            "sources": sources,
            "personality": personality
        },
        color = create_color()
    )
    user.digests.append(digest)
    db.session.add(user)
    db.session.commit()

    return {"id": str(user.id)}, 200

@auth.route('/logout', methods = ["GET", "POST"])
@jwt_required()
def logout():

    return {"message": "Signed out."}, 200

@auth.route("/refresh")
@jwt_required(refresh = True)
def refresh():
    
    current_user = get_jwt_identity()
    token = create_access_token(identity = current_user, fresh = False)

    return {"access_token": token}, 200