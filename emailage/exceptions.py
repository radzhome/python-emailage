"""
emailAge exception handling module.
"""


class EmailAgeServiceException(Exception):
    """
    Exception: Serves as the exception handler for emailAge requests.
    """

    def __init__(self, error_code, value):
        self.error_code = error_code
        self.value = value

    def __unicode__(self):
        return "%s (Error code: %s)" % (repr(self.value), self.error_code)

    def __str__(self):
        return self.__unicode__()
