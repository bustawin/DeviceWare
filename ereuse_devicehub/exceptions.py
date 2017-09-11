from typing import List

from bson import ObjectId


class BasicError(Exception):
    status_code = None

    def __init__(self, body: dict or str, status_code: int = 500):
        self.body = body
        if self.status_code is None:
            self.status_code = status_code

    def to_dict(self):
        return self.body


class StandardError(BasicError):
    message = None

    def __init__(self, message="", status_code=None):
        if self.message is None:
            self.message = message
        self.status_code = status_code or self.status_code

    def to_dict(self):
        return {
            '_error': {
                'message': self.message,
                'code': self.status_code,
                '@type': type(self).__name__
            },
            '_issues': {
                type(self).__name__: self.message
            },
            '_status': 'ERR'
        }


class SchemaError(StandardError):
    status_code = 422

    def __init__(self, field=None, message=None):
        if field:
            self.field = field
        if message:
            self.message = message

    def to_dict(self):
        d = super().to_dict()
        # We are missing what we add in line 28 of this file, but this is needed to follow Cerberus' errors
        # todo change this when changing Cerberus' errors
        d['_issues'] = {
            self.field: self.message
        }
        return d


class UnauthorizedToUseDatabase(StandardError):
    status_code = 401
    message = 'User has no access to this database.'


class InsufficientDatabasePerm(StandardError):
    status_code = 401

    def __init__(self, resource_name: str, db: str, _id: str or ObjectId):
        from ereuse_devicehub.resources.account.domain import AccountDomain
        db = db or AccountDomain.requested_database
        message = 'Account has not enough database access {} {} in {}.'.format(resource_name, _id, db)
        super().__init__(message)


class UserHasExplicitDbPerms(SchemaError):
    def __init__(self, db: str, resource_id: str, resource_type: str, accounts: List[dict]):
        field = 'perms'
        message = 'Cannot share {} {} with accounts {} as they have full (explicit) access to the database already.' \
            .format(resource_type, resource_id, pluck(accounts, 'email'))
        super().__init__(field, message)


class InnerRequestError(BasicError):
    """
    Encapsulates errors produced by internal requests (GET, POST...).
    """

    def __init__(self, status_code, info: dict = None):
        self.info = info
        super().__init__(info, status_code)


class WrongCredentials(StandardError):
    """
    Error when login and user/pass do not match.
    """
    status_code = 401
    message = 'There is not an user with the matching username/password'


class RedirectToClient(Exception):
    """
    An exception that forces a redirection to the client.
    """
    pass


class RequestAnother(BasicError):
    """Redirects to DELETE Snapshot"""


class WrongQueryParam(SchemaError):
    pass
