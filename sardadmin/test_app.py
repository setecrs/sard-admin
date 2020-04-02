import unittest
import jwt

from .app import create_app, check_admin, check_auth, check_member, check_user
from .auth import Auth, ExceptionWrongUserPass

def check_bind_ok(server, user, password):
    return

def check_bind_fail(server, user, password):
    raise ExceptionWrongUserPass()

class TestCheckAuth(unittest.TestCase):

    def test_check_auth_ok(self):
        app = create_app('test', 'jwtsecret')
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        token = auth.login('asdf1234', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            user = check_auth(ctx.request,auth)
            self.assertEqual(user, 'asdf1234')

    def test_check_auth_invalid_token(self):
        app = create_app('test', 'jwtsecret')
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        token = auth.login('asdf1234', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token[:-4]}'
        )) as ctx:
            with self.assertRaises(jwt.exceptions.DecodeError):
                check_auth(ctx.request,auth)
