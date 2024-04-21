class APIException(Exception):
    pass

class ObjectNotFoundException(APIException):
    pass

class InvalidRequestException(APIException):
    pass
