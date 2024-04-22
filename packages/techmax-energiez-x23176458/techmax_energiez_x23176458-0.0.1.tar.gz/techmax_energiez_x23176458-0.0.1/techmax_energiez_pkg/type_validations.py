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

# Example Usage:
if __name__ == "__main__":
    validator = TypeValidator()
    
    # String Validation with min and max length
    string_value = "Hello, World!"
    print(f"Is '{string_value}' a valid string with length between 5 and 15? "
          f"{validator.string_type_validator(string_value, min_length=5, max_length=15)}")
    string_value = "Hello, World!"
    print(f"Is '{string_value}' a valid string with length between 5 and 15? "
          f"{validator.string_type_validator(string_value, min_length=2, max_length=10)}")
    string_value = "He"
    print(f"Is '{string_value}' a v"
          f"{validator.string_type_validator(string_value, min_length=5, max_length=15)}")

    # Number Validation with min and max values
    number_value = 123.45
    print(f"Is '{number_value}' a valid number between 100 and 200? "
          f"{validator.number_type_validator(number_value, min_number=100, max_number=200)}")
    number_value = 99.00
    print(f"Is '{number_value}' a valid number between 100 and 200? "
          f"{validator.number_type_validator(number_value, min_number=100, max_number=200)}")
    number_value = 175
    print(f"Is '{number_value}' a valid number between 100 and 200? "
          f"{validator.number_type_validator(number_value, min_number=100, max_number=200)}")

