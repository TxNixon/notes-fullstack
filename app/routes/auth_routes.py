from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user

register_bp = Blueprint('register_bp', __name__)
login_bp = Blueprint('login_bp', __name__)

@register_bp.route('/', methods=['POST'])
def register():
    #get resuest dulu json nya
    data = request.get_json()

    #cek validasi
    required_data = ["username", "email", "password"]

    if not all(fields in data and data[fields] for fields in required_data):
        return jsonify({"error": "Missing required fields"}), 422
    
    # call register service
    result = register_user(
        input_username=data["username"],
        input_email=data["email"],
        input_password=data["password"]
    )
    
    # result contains either {"error": "..."} or {"message": "..."} and a status code
    response, status_code = result
    return jsonify(response), status_code

@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()

    required_data = ["username", "password"]

    if not all(fields in data and data[fields] for fields in required_data):
        return jsonify({"error": "Missing required fields"}), 422

    user_data, msg = login_user(data["username"], data["password"])

    if not user_data:
        return jsonify({"error": msg}), 401
    
    return jsonify({
        "data" : user_data
    }), 200