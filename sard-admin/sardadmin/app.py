#!/usr/bin/env python3

import os
import http
import logging
from flask import Flask, make_response, request
from flask_restplus import Resource, Api, fields
from werkzeug.exceptions import BadRequest

from .user import  User
from .group import  Group
from .auth import  Auth
from .check_request import CheckRequest

DEBUG=('DEBUG' in os.environ)

def create_app(ldap_server=None, jwt_secret=None):
    if ldap_server is None:
        ldap_server = os.environ['LDAP_SERVER']
    assert len(ldap_server) > 0
    if jwt_secret is None:
        jwt_secret = os.environ['JWT_SECRET']
    assert len(jwt_secret) > 0
    auth = Auth(jwt_secret, ldap_server)
    return _create_app(auth, User, Group)

def _create_app(auth, User, Group):
    app = Flask(__name__)           #  Create a Flask WSGI appliction
    api = Api(app)                  #  Create a Flask-RESTPlus API
    check_request = CheckRequest(auth, User, Group)
    log = logging.getLogger(__name__)

    @api.route('/jobs/')
    class Jobs(Resource):
        def get(self):
            return {
                "history": [dict((k,h[k]) for k in h if k != 'thread') for h in Group.history],
                "jobs": dict([(op, dict((k,Group.jobs[op][k]) for k in Group.jobs[op] if k != 'thread')) for op in Group.jobs]),
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
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/group/<string:group>')
    class GroupNewRoute(Resource):
        def get(self, group):
            """Lista membros do grupo"""
            try:
                return Group(group).users()
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

        def post(self, group):
            """Cria novo grupo"""
            try:
                check_request.check_admin(request)
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                return (dict(error=str(e)), http.HTTPStatus.UNAUTHORIZED)
            try:
                Group(group).create()
                return ('', http.HTTPStatus.NO_CONTENT)
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/group/<string:group>/permissions')
    class GroupPermsRoute(Resource):
        @api.representation('text/plain')
        def post(self, group):
            """Verifica e corrige permissoes do grupo"""
            try:
                check_request.check_member(group, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                return Group(group).permissions()
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/user/')
    class UserListRoute(Resource):
        def get(self):
            """Lista todos os usuarios"""
            try:
                return {
                    'users': User.listAll(),
                }
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

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
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))
        @api.representation('text/plain')
        def post(self, login):
            """Cria novo usuario"""
            try:
                check_request.check_admin(request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                return dict(password=User(login).create())
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/user/<string:login>/group/<string:group>')
    class UserGroupRoute(Resource):
        @api.representation('text/plain')
        def post(self, login, group):
            """Adiciona usuario ao grupo"""
            try:
                check_request.check_member(group, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                User(login).enterGroup(group)
                return ('', 204)
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/user/<string:login>/home')
    class UserHomeRoute(Resource):
        @api.representation('text/plain')
        def post(self, login):
            """Verifica e corrige pasta home do usuario"""
            try:
                check_request.check_user(login, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                User(login).populateHome()
                return ('', 204)
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/user/<string:login>/permissions')
    class UserPermissionsRoute(Resource):
        @api.representation('text/plain')
        def post(self, login):
            """Verifica e corrige permissoes do usuario"""
            try:
                check_request.check_user(login, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                User(login).permissions()
                return ('', 204)
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/user/<string:login>/reset_password')
    class UserPasswordRoute(Resource):
        @api.representation('text/plain')
        @api.expect(api.model('data', {
            "password": fields.String(required=False, description='password'),
        }))
        def post(self, login):
            """Altera a senha do usuario. Se a senha for "", uma senha aleatoria sera criada."""
            try:
                check_request.check_user(login, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                return {
                    "password": User(login).resetPassword(api.payload['password'])
                }
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/auth/login')
    class AuthLogin(Resource):
        @api.representation('text/plain')
        @api.expect(api.model('data', dict(
            user=fields.String(required=True, description='user'),
            password=fields.String(required=True, description='password'),
        )))
        def post(self):
            try:
                user = api.payload['user']
                password = api.payload['password']
            except:
                raise BadRequest('must send user and password')
            try:
                token = auth.login(user, password, seconds=300)
                return dict(auth_token=token.strip())
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/auth/logout/')
    class AuthLogin(Resource):
        def get(self):
            try:
                user = check_request.check_auth(request)
            except:
                return ('', http.HTTPStatus.BAD_REQUEST)
            auth.logout(user)
            return ('', 204)

    return app