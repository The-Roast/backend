from datetime import datetime
from flask import Blueprint, request, redirect, url_for, jsonify, session
from flask_jwt_extended import create_access_token
from ...extensions import db
from ...db.schemas import Digests, Users, create_color

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST'])
def login():
    
    email = request.json["email"]

    user: Users = Users.query.filter_by(email = email).first()
    if not user:
        return jsonify({
            "message": "Invalid email.",
            "status": 404
        })
    
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)

    return jsonify({
        "message": access_token,
        "status": 200
    })

@auth.route('/signup', methods = ['POST'])
def signup():

    email = request.json["email"]
    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    digest_name = request.json["digestName"]
    interests = request.json["interests"]
    sources = request.json["contentSources"]
    personality = request.json["personality"]

    user = Users.query.filter_by(email = email).first()

    if user:
        return jsonify({
            "message": "Use a different email.",
            "status": 404
        })
    
    user = Users(
        email = email,
        first_name = first_name,
        last_name = last_name,
    )
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

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    
    return jsonify({
        "message": access_token,
        "status": 200
    })

# @auth.route('/logout', methods = ["GET"])
# @jwt_required
# def logout():

#     return {
#         "message": "Signed out.",
#         "status": 200
#     }