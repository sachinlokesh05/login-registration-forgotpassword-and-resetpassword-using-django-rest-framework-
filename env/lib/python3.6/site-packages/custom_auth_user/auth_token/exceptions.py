# -*- coding: utf-8
from datetime import datetime


class AuthenticationFailed(Exception):
    """
    Login/Authentication failed
    or
    User unauthenticated
    Authentication not provided
    """

    def __init__(self, message='Authentication Failed'):
        super(AuthenticationFailed, self).__init__(message)
        self.when = datetime.now()


class TokenNotFound(Exception):
    """
    Token not found
    """

    def __init__(self, message='Token not found'):
        super(TokenNotFound, self).__init__(message)
        self.when = datetime.now()
