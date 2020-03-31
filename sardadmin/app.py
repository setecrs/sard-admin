#!/usr/bin/env python3

import os
import http
import logging
from flask import Flask, make_response, request
from flask_restplus import Resource, Api, fields
from werkzeug.exceptions import BadRequest

from .user import User
from .group import Group, jobs, history
from .auth import Auth

def create_app(ldap_server=None, jwt_secret=None):
    app = Flask(__name__)                          #  Create a Flask WSGI appliction
    api = Api(app, default_mediatype='text/plain') #  Create a Flask-RESTPlus API
    if ldap_server is None:
        ldap_server = os.environ['LDAP_SERVER']
    assert len(ldap_server) > 0
    if jwt_secret is None:
        jwt_secret = os.environ['JWT_SECRET']
    assert len(jwt_secret) > 0
    auth = Auth(jwt_secret, ldap_server)

    def check_auth(request: Flask.request_class):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(' ',1)[1]
        user = auth.check(auth_token)
        return user
    
    def check_admin(request: Flask.request_class):
        user = check_auth(request)
        if not user in Group('Domain Admins').users():
            raise Exception('User must be in group "Domain Admins" to use this resource')

    def check_member(group, request: Flask.request_class):
        user = check_auth(request)
        if (not user in Group('Domain Admins').users() and
            not user in Group(group).users()):
            raise Exception('User must be a member or be in group "Domain Admins" to use this resource')

    def check_user(user, request: Flask.request_class):
        auth_user = check_auth(request)
        if (not auth_user in Group('Domain Admins').users() and
            not auth_user == user):
            raise Exception('User must be himself or be in group "Domain Admins" to use this resource')

    @api.route('/jobs/', methods=['GET'])
    class Jobs(Resource):
        def get(self):
            return {
                "history": [dict((k,h[k]) for k in h if k != 'thread') for h in history],
                "jobs": dict([(op, dict((k,jobs[op][k]) for k in jobs[op] if k != 'thread')) for op in jobs]),
                }

    @api.route('/group/')
    class GroupRoute(Resource):
        def get(self):
            """Lista todos os grupos"""
            try:
                return {
                    'groups': Group.listAll(),
                }
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/group/<string:group>')
    class GroupNewRoute(Resource):
        def get(self, group):
            """Lista membros do grupo"""
            try:
                return Group(group).users()
            except Exception as e:
                raise BadRequest(str(e))

        @api.representation('text/plain')
        def post(self, group):
            """Cria novo grupo"""
            log = logging.getLogger(__name__)
            try:
                check_admin(request)
            except Exception as e:
                log.exception(e)
                return make_response(str(e), http.HTTPStatus.UNAUTHORIZED)
            try:
                Group(group).create()
                return ('', 204)
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/group/<string:group>/permissions')
    class GroupPermsRoute(Resource):
        @api.representation('text/plain')
        def post(self, group):
            """Verifica e corrige permissoes do grupo"""
            try:
                check_member(group, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                return Group(group).permissions()
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/user/')
    class UserListRoute(Resource):
        def get(self):
            """Lista todos os usuarios"""
            try:
                return {
                    'users': User.listAll(),
                }
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/user/<string:login>')
    class UserCreateRoute(Resource):
        def get(self, login):
            """Lista grupos do usuario"""
            try:
                return {
                    'user': login,
                    'groups': User(login).groups(),
                }
            except Exception as e:
                raise BadRequest(str(e))
        @api.representation('text/plain')
        def post(self, login):
            """Cria novo usuario"""
            try:
                check_admin(request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                return User(login).create()
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/user/<string:login>/group/<string:group>')
    class UserGroupRoute(Resource):
        @api.representation('text/plain')
        def post(self, login, group):
            """Adiciona usuario ao grupo"""
            try:
                check_member(group, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                User(login).enterGroup(group)
                return ('', 204)
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/user/<string:login>/home')
    class UserHomeRoute(Resource):
        @api.representation('text/plain')
        def post(self, login):
            """Verifica e corrige pasta home do usuario"""
            try:
                check_user(login, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                User(login).populateHome()
                return ('', 204)
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/user/<string:login>/permissions')
    class UserPermissionsRoute(Resource):
        @api.representation('text/plain')
        def post(self, login):
            """Verifica e corrige permissoes do usuario"""
            try:
                check_user(login, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                User(login).permissions()
                return ('', 204)
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/user/<string:login>/reset_password')
    class UserPasswordRoute(Resource):
        @api.representation('text/plain')
        @api.expect(api.model('data', {
            "password": fields.String(required=False, description='password'),
        }))
        def post(self, login):
            """Altera a senha do usuario. Se a senha for "", uma senha aleatoria sera criada."""
            try:
                check_user(login, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                return {
                    "password": User(login).resetPassword(api.payload['password'])
                }
            except Exception as e:
                raise BadRequest(str(e))

    @api.route('/auth/login')
    class AuthLogin(Resource):
        @api.representation('text/plain')
        @api.expect(api.model('data', dict(
            user=fields.String(required=True, description='user'),
            password=fields.String(required=True, description='password'),
        )))
        def post(self):
            log = logging.getLogger(__name__)
            try:
                user = api.payload['user']
                password = api.payload['password']
            except:
                raise BadRequest('must send user and password')
            try:
                token = auth.login(user, password, seconds=300)
                return dict(auth_token=token.strip())
            except Exception as e:
                log.exception(e)
                raise BadRequest(str(e))

    @api.route('/auth/logout/')
    class AuthLogin(Resource):
        @api.representation('text/plain')
        def get(self):
            try:
                user = check_auth(request)
            except:
                return ('', http.HTTPStatus.BAD_REQUEST)
            auth.logout(user)
            return ''

    return app
