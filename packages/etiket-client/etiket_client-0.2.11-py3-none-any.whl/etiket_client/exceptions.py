class LoginFailedException(Exception):
    pass

class TokenRefreshException(Exception):
    pass

class NoAccessTokenFoundException(Exception):
    pass

class RequestFailedException(Exception):
    pass

class SchemaNotValidException(Exception):
    pass