import unittest
import time
import jwt

from .auth import Auth, ExceptionWrongUserPass

def check_bind_ok(server, user, password):
    return

def check_bind_fail(server, user, password):
    raise ExceptionWrongUserPass

class TestAuth(unittest.TestCase):
    def test_login_ok(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        token = auth.login('asdf1234', 'pass', 300)
        self.assertIsInstance(token, str)

    def test_login_fail(self):
        auth = Auth('secret', 'test', check_bind=check_bind_fail)
        with self.assertRaises(ExceptionWrongUserPass):
            token = auth.login('asdf1234', 'pass', 300)

    def test_check_ok(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        token = auth.login('user1234', 'pass', 300)
        user = auth.check(token)
        self.assertEqual(user, 'user1234')

    def test_check_fake_token(self):
        auth1 = Auth('secret1', 'test', check_bind=check_bind_ok)
        auth2 = Auth('secret2', 'test', check_bind=check_bind_ok)
        token = auth1.login('user1234', 'pass', 300)
        with self.assertRaises(jwt.exceptions.InvalidSignatureError):
            auth2.check(token)

    def test_check_invalid_token(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        token = ''
        with self.assertRaises(jwt.exceptions.DecodeError):
            auth.check(token)

    def test_check_expired(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        token = auth.login('user1234', 'pass', 0)
        time.sleep(1) # minimun exp-iat == 1 second
        with self.assertRaises(jwt.exceptions.ExpiredSignature):
            auth.check(token)

    def test_check_invalidated(self):
        auth = Auth('secret', 'test', check_bind=check_bind_ok)
        token = auth.login('user1234', 'pass', 300)
        auth.logout('user1234')
        with self.assertRaises(jwt.exceptions.ExpiredSignature):
            auth.check(token)

