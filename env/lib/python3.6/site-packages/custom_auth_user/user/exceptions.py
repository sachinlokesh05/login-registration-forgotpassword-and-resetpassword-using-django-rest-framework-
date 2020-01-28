# -*- coding: utf-8
from datetime import datetime


class InvalidInput(Exception):
    """
    Invalid input
    """

    def __init__(self, message='Invalid input'):
        super(InvalidInput, self).__init__(message)
        self.when = datetime.now()
