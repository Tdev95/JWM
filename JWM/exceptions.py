class JWMException(Exception):
    pass


class InvalidHeaderException(JWMException):
    pass


class MissingBodyException(JWMException):
    pass
