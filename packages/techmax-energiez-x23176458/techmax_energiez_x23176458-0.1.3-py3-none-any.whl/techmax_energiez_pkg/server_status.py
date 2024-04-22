import json

class ServerResponse:
    @staticmethod
    def success_response(data=None, message="Success"):
        response_data = {
            "status": 200,
            "message": message,
            "data": data
        }
        return json.dumps(response_data)

    @staticmethod
    def forbidden_response(message="Forbidden"):
        response_data = {
            "status": 403,
            "message": message
        }
        return json.dumps(response_data)

    @staticmethod
    def not_found_response(message="Not Found"):
        response_data = {
            "status": 404,
            "message": message
        }
        return json.dumps(response_data)

    @staticmethod
    def internal_server_error_response(message="Internal Server Error"):
        response_data = {
            "status": 500,
            "message": message
        }
        return json.dumps(response_data)
