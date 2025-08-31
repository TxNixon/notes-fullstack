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
def edit_user():
    current_user_id = get_jwt_identity()
    data = request.form.to_dict()
    #untuk ambil data request
    profile_image_file = request.files.get('profile_image')
    thumbnail_img_file = request.files.get('thumbnail_img')

    #untuk validasi data jika tidak ada data sama sekali
    if not data and not profile_image_file and not thumbnail_img_file:
        return error_response("No data provided", 400)
    
    #call service update user
    user, message = update_user(current_user_id, data, profile_image_file, thumbnail_img_file)

    #jika gagal update user
    if not user:
        return error_response(message, 400)

    return success_response(user, message, 200)