class TypeValidator:
    @staticmethod
    def string_type_validator(value, min_length=None, max_length=None):
        if not isinstance(value, str):
            return False
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        return bool(value.strip())

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