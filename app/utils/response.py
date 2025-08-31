from flask import jsonify

def success_response(data=None, message="Success", status_code=200, meta=None):
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    if meta is not None:
        response["meta"] = meta
    return jsonify(response), status_code

def error_response(message="Error", status_code=400):
    response = {
        "status": "error",
        "message": message
    }
    return jsonify(response), status_code
