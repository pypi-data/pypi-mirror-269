from .server_status import ServerResponse

class TypeValidator:
    @staticmethod
    def string_type_validator(value, min_length=None, max_length=None):
        if not isinstance(value, str):
            return ServerResponse.forbidden_response("Value is not a string.")
        
        if min_length is not None and len(value) < min_length:
            return ServerResponse.forbidden_response(f"String length should be at least {min_length} characters.")
        
        if max_length is not None and len(value) > max_length:
            return ServerResponse.forbidden_response(f"String length should be at most {max_length} characters.")
        
        if not value.strip():
            return ServerResponse.forbidden_response("String should not be empty.")
        
        return True

    @staticmethod
    def number_type_validator(value, min_number=None, max_number=None):
        if isinstance(value, int):
            value = float(value)
        
        if not isinstance(value, float):
            return ServerResponse.forbidden_response("Value is not a number.")
        
        if min_number is not None and value < min_number:
            return ServerResponse.forbidden_response(f"Number should be greater than or equal to {min_number}.")
        
        if max_number is not None and value > max_number:
            return ServerResponse.forbidden_response(f"Number should be less than or equal to {max_number}.")
        
        return True
