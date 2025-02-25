from flask import jsonify

def handle_bad_request(error):
    return jsonify({"message": "Bad request"}), 400

def handle_unauthorized(error):
    return jsonify({"message": "Unauthorized"}), 401

def handle_not_found(error):
    return jsonify({"message": "Resource not found"}), 404

def handle_internal_server_error(error):
    return jsonify({"message": "Internal server error"}), 500