from app.services.user_service import get_user_by_id, update_user
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.response import success_response, error_response

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()

    user, message = get_user_by_id(current_user_id)

    if not user:
        return error_response(message, 404)

    return success_response(user, message, 200)

@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user_route():
    current_user_id = get_jwt_identity()
    data = request.json

    user, message = update_user(current_user_id, data)

    if not user:
        return error_response(message, 400)

    return success_response(user, message, 200)