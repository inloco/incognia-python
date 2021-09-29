from requests import HTTPError


class IncogniaError(Exception):
    pass


class IncogniaHTTPError(HTTPError):
    pass
