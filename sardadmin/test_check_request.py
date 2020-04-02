import unittest
import jwt

from .check_request import CheckRequest, UnauthorizedException
from .auth import Auth, ExceptionWrongUserPass
from .app import _create_app

def check_bind_ok(server, user, password):
    return

def check_bind_fail(server, user, password):
    raise ExceptionWrongUserPass()

class MockUser:
    def __init__(self, user):
        self.user = user

class MockGroup:
    def __init__(self, group):
        self.group = group

    def users(self):
        if self.group ==  'Domain Admins':
            return ['admin']
        if self.group == 'group1':
            return ['user1']

class TestCheckAuth(unittest.TestCase):

    def test_check_auth_ok(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('asdf1234', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            user = cr.check_auth(ctx.request)
            self.assertEqual(user, 'asdf1234')

    def test_check_auth_invalid_token(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('asdf1234', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token[:-4]}'
        )) as ctx:
            with self.assertRaises(jwt.exceptions.DecodeError):
                cr.check_auth(ctx.request)

    def test_check_admin_not_admin(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('asdf1234', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            with self.assertRaises(UnauthorizedException):
                cr.check_admin(ctx.request)

    def test_check_admin_admin(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('admin', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            cr.check_admin(ctx.request)

    def test_check_member_strange(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('strange', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            with self.assertRaises(UnauthorizedException):
                cr.check_member('group1', ctx.request)

    def test_check_member_user1(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('user1', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            cr.check_member('group1', ctx.request)

    def test_check_member_admin(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('admin', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            cr.check_member('group1', ctx.request)

    def test_check_user_strange(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('strange', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            with self.assertRaises(UnauthorizedException):
                cr.check_user('user1', ctx.request)

    def test_check_user_user1(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('user1', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            cr.check_user('user1', ctx.request)

    def test_check_user_admin(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        cr = CheckRequest(auth, MockUser, MockGroup)
        app = _create_app(auth, MockUser, MockGroup)
        token = auth.login('admin', 'pass', 300)
        with app.test_request_context('http://api:80/group/add', data='', headers=dict(
            Authorization=f'Bearer {token}'
        )) as ctx:
            cr.check_user('user1', ctx.request)
