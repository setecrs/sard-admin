class CheckRequest:
    def __init__(self, auth, User, Group):
        self.auth=auth
        self.User=User
        self.Group=Group

    def check_auth(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise UnauthorizedException('Request must have an Authorization header')
        auth_token = auth_header.split(' ',1)[1]
        user = self.auth.check(auth_token)
        return user

    def check_admin(self, request):
        user = self.check_auth(request)
        if not user in self.Group('Domain Admins').users():
            raise UnauthorizedException('User must be in group "Domain Admins" to use this resource')

    def check_member(self, group, request):
        user = self.check_auth(request)
        if (not user in self.Group('Domain Admins').users() and
            not user in self.Group(group).users()):
            raise UnauthorizedException('User must be a member or be in group "Domain Admins" to use this resource')

    def check_user(self, user, request):
        auth_user = self.check_auth(request)
        if (not auth_user in self.Group('Domain Admins').users() and
            not auth_user == user):
            raise UnauthorizedException('User must be himself or be in group "Domain Admins" to use this resource')

class UnauthorizedException(Exception):
    """Unauthorized"""
    pass
