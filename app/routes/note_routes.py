from flask import Blueprint, jsonify, request
from app.services.note_service import create_note
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        return jsonify({
            "message": message,
            "data": note.to_json()
        }), 201
    return jsonify({"error": message}), 400
