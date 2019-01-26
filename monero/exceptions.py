class JellyfinException(Exception):
    pass

class JellyfinBadRequest(JellyfinException):
    pass

class JellyfinUnauthorized(JellyfinException):
    pass

class JellyfinForbidden(JellyfinException):
    pass

class JellyfinResourceNotFound(JellyfinException):
    pass

class JellyfinServerError(JellyfinException):
    pass