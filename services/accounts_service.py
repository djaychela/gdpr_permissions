from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from pyramid.authentication import AuthTktAuthenticationPolicy
from passlib.hash import pbkdf2_sha256


class AccountsService():
    @staticmethod
    def check_password_hash(password, hash):
        return pbkdf2_sha256.verify(password, hash)

    @staticmethod
    def create_password_hash(password):
        hash = pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=16)
        return hash

    # @staticmethod
    # def groupfinder(userid, request):
    #     user =


class DatabaseRecordFactory(object):
    __acl__ = [(Allow, Authenticated, 'view'),
               (Allow, 'admin', ALL_PERMISSIONS),]

    def __init__(self, request):
        pass


class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self,request):
        user = request.user
        if user is not None:
            return user.id

    def effective_principals(self, request):
        principals = [Everyone]
        user = request.user
        if user is not None:
            principals.append(Authenticated)
            principals.append(str(user.id))
            principals.append('role:' + user.role)
        return principals

