#!/usr/bin/env python3

import os
import http
import logging
from flask import Flask, make_response, request
from flask_restplus import Resource, Api, fields
from werkzeug.exceptions import BadRequest

from .user import User
from .group import Group
from .auth import Auth
from .check_request import CheckRequest
from .k8s import K8s, getMetrics
from .folders import count_sard_folders, rename_sard_folder
from .job import listHistoryByName

DEBUG = ('DEBUG' in os.environ)


def create_app(ldap_server=None, jwt_secret=None):
    if ldap_server is None:
        ldap_server = os.environ['LDAP_SERVER']
    assert len(ldap_server) > 0
    if jwt_secret is None:
        jwt_secret = os.environ['JWT_SECRET']
    assert len(jwt_secret) > 0
    auth = Auth(jwt_secret, ldap_server)
    return _create_app(auth, User, Group)


def env2dict(env: str):
    result = {}
    for line in env.split('\n'):
        line = line.strip()
        if not line:
            continue
        parts = line.split('=', 1)
        if len(parts) == 2:
            result[parts[0]] = parts[1]
    return result


def _create_app(auth, User, Group):
    app = Flask(__name__)  # Create a Flask WSGI appliction
    api = Api(app)  # Create a Flask-RESTPlus API
    check_request = CheckRequest(auth, User, Group)
    log = logging.getLogger(__name__)

    @api.route('/iped/')
    class Iped(Resource):
        @api.representation('text/plain')
        @api.expect(api.model('ipedParameters', {
            "image": fields.String(required=True, description='docker image'),
            "IPEDJAR": fields.String(required=True, description='path to the IPED.jar file'),
            "EVIDENCE_PATH": fields.String(required=True, description='path to a datasource, to create a single job'),
            "OUTPUT_PATH": fields.String(required=True, description='IPED output folder'),
            "IPED_PROFILE": fields.String(required=True, description='IPED profile'),
            "ADD_ARGS": fields.String(required=True, description='extra arguments to IPED'),
            "ADD_PATHS": fields.String(required=True, description='extra source paths to IPED'),
            "env": fields.String(required=True, description='extra envirnoment variables, one by line'),
        }))
        def post(self):
            """Create a new kubernetes job to run IPED"""
            try:
                image = api.payload['image']
                IPEDJAR = api.payload['IPEDJAR']
                EVIDENCE_PATH = api.payload['EVIDENCE_PATH']
                OUTPUT_PATH = api.payload['OUTPUT_PATH']
                IPED_PROFILE = api.payload['IPED_PROFILE']
                ADD_ARGS = api.payload['ADD_ARGS']
                ADD_PATHS = api.payload['ADD_PATHS']
                env = api.payload['env']
            except:
                raise BadRequest('missing parameters')
            try:
                check_request.check_admin(request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                env = env2dict(env)
                return K8s().addJob(image, IPEDJAR, EVIDENCE_PATH, OUTPUT_PATH, IPED_PROFILE, ADD_ARGS, ADD_PATHS, **env)
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/jobs/')
    class Jobs(Resource):
        def get(self):
            return {
                "jobs": [op for op in Group.jobs],
            }

    @api.route('/jobs/<string:job>')
    class GetJob(Resource):
        def get(self, job):
            return {
                "history": listHistoryByName(Group.history, job)
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
                return {
                    "group": group,
                    "users": Group(group).users(),
                }
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
                Group(group).permissions()
                return ('', http.HTTPStatus.NO_CONTENT)
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
                password = api.payload['password']
            except:
                raise BadRequest('must send password')
            try:
                check_request.check_user(login, request)
            except:
                return make_response('Unauthorized', http.HTTPStatus.UNAUTHORIZED)
            try:
                return {
                    "password": User(login).resetPassword(password)
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
    class AuthLogout(Resource):
        def get(self):
            try:
                user = check_request.check_auth(request)
            except:
                return ('', http.HTTPStatus.BAD_REQUEST)
            auth.logout(user)
            return ('', 204)

    @api.route('/workers/')
    class Workers(Resource):
        def get(self):
            """List IPED workers"""
            try:
                result = []
                workers = K8s().listWorkers()
                for w in workers:
                    x = dict(
                        name=w.name,
                        pod_ip=w.pod_ip,
                        host_ip=w.host_ip,
                        node_name=w.node_name,
                        ready=w.ready,
                        image=w.image,
                    )
                    try:
                        if not w.ready:
                            mdata = getMetrics(w.pod_ip)
                            x['evidence'] = mdata.evidence
                            x['processed'] = mdata.processed
                            x['found'] = mdata.found
                    except:
                        pass
                    result.append(x)
                return result
            except:
                return ('', http.HTTPStatus.BAD_REQUEST)

    @api.route('/folders/count')
    class FoldersCount(Resource):
        @api.expect(api.model('data', dict(
            imagepath=fields.String(required=True, description='imagepath'),
        )))
        def post(self):
            """Count number of SARD and SARD.old dirs in imagepath folder"""
            try:
                imagepath = api.payload['imagepath']
                return {
                    'result': count_sard_folders(imagepath)
                }
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    @api.route('/folders/rename')
    class FoldersRename(Resource):
        @api.expect(api.model('data', dict(
            imagepath=fields.String(required=True, description='imagepath'),
        )))
        def post(self):
            """Rename folder SARD to SARD.old[x]"""
            try:
                imagepath = api.payload['imagepath']
                return {
                    'result': rename_sard_folder(imagepath)
                }
            except Exception as e:
                if DEBUG:
                    log.exception(e)
                raise BadRequest(dict(error=str(e)))

    return app
