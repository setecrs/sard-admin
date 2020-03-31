import sys
import datetime
import jwt
from ldap3 import Server, Connection

from .group import Group

class Auth():
    def __init__(self, secret, ldap_server, ldap_suffix='ou=People,dc=setecrs,dc=dpf,dc=gov,dc=br'):
        self.secret = secret
        self.ldap_suffix = ldap_suffix
        self.server = Server(ldap_server)
        self.tokens = {}

    def login(self, user, password, seconds):
        uid=f'uid={user},{self.ldap_suffix}'
        conn = Connection(self.server, uid, password)
        if not conn.bind():
            raise Exception('Wrong username or password')
        token = dict(
            exp=datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds),
            iat=datetime.datetime.utcnow(),
            sub=user, 
        )
        self.tokens[user] = token
        return jwt.encode(token, key=self.secret, algorithm='HS256').decode('utf-8')

    def logout(self, user):
        del token[user]
    
    def check(self, encoded_token):
        token = jwt.decode(encoded_token, key=self.secret)
        user = token['sub']
        assert self.tokens[user]['exp'] == token['exp']
        assert self.tokens[user]['iat'] == token['iat']
        return user