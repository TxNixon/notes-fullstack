from flask import Blueprint, jsonify, request
from app.services.note_service import create_note, get_public_notes
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.response import success_response, error_response

note_bp = Blueprint("note_bp", __name__)

@note_bp.route("/", methods=["POST"])
@jwt_required()

def add_note():
    data = request.json
    user_id = get_jwt_identity()

    # Validasi data yang diperlukan
    required_fields = ["title", "content", "status"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    note, message = create_note(
        user_id=user_id,
        title=data["title"],
        content=data["content"],
        status=data["status"],
        password_hash=data.get("password"),
        password_hint=data.get("password_hint")
    )
    if note:
        return success_response(message, note.to_json())
    return error_response(message)


@note_bp.route('/', methods=['GET'])

def public_notes():
    q = request.args.get('q', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort = request.args.get('sort', 'created_at', type=str)
    order = request.args.get('order', 'desc', type=str)

    notes, meta, message = get_public_notes(q=q, page=page, per_page=per_page, sort=sort, order=order)

    return success_response(message, notes, meta=meta, status_code=200)