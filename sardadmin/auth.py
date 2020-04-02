import sys
import datetime
import jwt
from ldap3 import Server, Connection

from .group import Group

def check_bind(server, uid, password):
    conn = Connection(server, uid, password)
    if not conn.bind():
        raise ExceptionWrongUserPass
    conn.unbind()

class Auth():
    def __init__(self, secret, ldap_server, ldap_suffix='ou=People,dc=setecrs,dc=dpf,dc=gov,dc=br', check_bind=check_bind):
        self.secret = secret
        self.ldap_suffix = ldap_suffix
        self.check_bind = check_bind
        self.server = Server(ldap_server)
        self.tokens = {}

    def login(self, user, password, seconds):
        uid=f'uid={user},{self.ldap_suffix}'
        self.check_bind(self.server, uid, password)
        iat = datetime.datetime.utcnow()
        token = dict(
            exp=iat + datetime.timedelta(seconds=seconds),
            iat=iat,
            sub=user, 
        )
        self.tokens[user] = token
        return jwt.encode(token, key=self.secret, algorithm='HS256').decode('utf-8')

    def logout(self, user):
        del self.tokens[user]
    
    def check(self, encoded_token):
        token = jwt.decode(encoded_token, key=self.secret, algorithms=['HS256'])
        user = token['sub']
        if not user in self.tokens:
            raise jwt.exceptions.ExpiredSignatureError
        try:
            assert self.tokens[user]['exp'] == token['exp']
            assert self.tokens[user]['iat'] == token['iat']
        except:
            raise jwt.exceptions.ExpiredSignatureError
        return user

class ExceptionWrongUserPass(Exception):
    """Wrong username or password"""
    pass
