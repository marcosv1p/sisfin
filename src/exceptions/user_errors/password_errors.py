from src.exceptions.user_errors.generic_user_error import GenericUserError
from src.exceptions.error_codes import ErrorCodes

class PasswordLengthError(GenericUserError):
    def __init__(self):
        error_details = ErrorCodes.PASSWORD_TOO_SHORT.to_dict()
        super().__init__(error_details['code'], error_details['message'])

class PasswordUppercaseError(GenericUserError):
    def __init__(self):
        error_details = ErrorCodes.PASSWORD_MISSING_UPPERCASE.to_dict()
        super().__init__(error_details['code'], error_details['message'])

class PasswordLowercaseError(GenericUserError):
    def __init__(self):
        error_details = ErrorCodes.PASSWORD_MISSING_LOWERCASE.to_dict()
        super().__init__(error_details['code'], error_details['message'])

class PasswordDigitError(GenericUserError):
    def __init__(self):
        error_details = ErrorCodes.PASSWORD_MISSING_DIGIT.to_dict()
        super().__init__(error_details['code'], error_details['message'])

class PasswordSpecialCharError(GenericUserError):
    def __init__(self):
        error_details = ErrorCodes.PASSWORD_MISSING_SPECIAL_CHAR.to_dict()
        super().__init__(error_details['code'], error_details['message'])
