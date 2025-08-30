from app.models.user import User
from app import db
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

def register_user(input_username, input_email, input_password):
    try:
        # Check if username exists
        if User.query.filter_by(username=input_username).first():
            return {"error": "Username already exists"}, 409
        
        # Check if email exists
        if User.query.filter_by(email=input_email).first():
            return {"error": "Email already exists"}, 409

        # Create new user
        new_user = User(username=input_username, email=input_email)
        new_user.set_password(input_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return {
            "message": "User registered successfully",
            "user": {
                "username": new_user.username,
                "email": new_user.email
            }
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    

def login_user(input_username, input_password):
    user = User.query.filter_by(username=input_username).first()
    if not user:
        return None, "User not found"

    if not user.check_password(input_password):
        return None, "User or password is invalid"

    token = create_access_token(identity=str(user.id))

    user_data = {
        "username": user.username,
        "email": user.email,
        "token": token,
        "profile_image": user.profile_image,
        "thumbnail_img": user.thumbnail_img
    }

    return user_data, "Login successful"
