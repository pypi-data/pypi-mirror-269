from flask import jsonify

class ServerResponse:
    @staticmethod
    def success_response(data=None, message="Success"):
        return jsonify({
            "status": 200,
            "message": message,
            "data": data
        })

    @staticmethod
    def forbidden_response(message="Forbidden"):
        return jsonify({
            "status": 403,
            "message": message
        })

    @staticmethod
    def not_found_response(message="Not Found"):
        return jsonify({
            "status": 404,
            "message": message
        })

    @staticmethod
    def internal_server_error_response(message="Internal Server Error"):
        return jsonify({
            "status": 500,
            "message": message
        })
