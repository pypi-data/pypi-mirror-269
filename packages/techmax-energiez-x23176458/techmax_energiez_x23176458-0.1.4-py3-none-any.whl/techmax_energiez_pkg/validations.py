import re

class TypeValidator:
    @staticmethod
    def string_type_validator(value, min_length=None, max_length=None):
        if not isinstance(value, str):
            return False
        
        if min_length is not None and len(value) < min_length:
            return False
        
        if max_length is not None and len(value) > max_length:
            return False
        
        if not value.strip():
            return False
        
        return True

    @staticmethod
    def number_type_validator(value, min_number=None, max_number=None):
        if isinstance(value, int):
            value = float(value)
        
        if not isinstance(value, float):
            return False
        
        if min_number is not None and value < min_number:
            return False
        
        if max_number is not None and value > max_number:
            return False
        
        return True

    @staticmethod
    def password_validator(value, min_length=8, max_length=32):
        if not TypeValidator.string_type_validator(value, min_length=min_length, max_length=max_length):
            return False
        
        if not re.match(r"^[a-zA-Z0-9!@#$%^&*()_+{}\[\]:;<>,.?/~\-=|\\]{8,32}$", value):
            return False
        
        return True

    @staticmethod
    def username_validator(value, min_length=4, max_length=20):
        if not TypeValidator.string_type_validator(value, min_length=min_length, max_length=max_length):
            return False
        
        if not re.match(r"^[a-zA-Z0-9_-]{4,20}$", value):
            return False
        
        return True

    @staticmethod
    def email_validator(value):
        if not TypeValidator.string_type_validator(value):
            return False
        
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            return False
        
        return True

    @staticmethod
    def url_validator(value):
        if not TypeValidator.string_type_validator(value):
            return False
        
        if not re.match(r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/?", value):
            return False
        
        return True
