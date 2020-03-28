#!/usr/bin/env python3

from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.exceptions import BadRequest

from sardadmin.user import User
from sardadmin.group import Group, jobs, history

app = Flask(__name__)                  #  Create a Flask WSGI appliction
api = Api(app, default_mediatype='text/plain')                         #  Create a Flask-RESTPlus API

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
            User(login).create()
            return ('', 204)
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/user/<string:login>/group/<string:group>')
class UserGroupRoute(Resource):
    @api.representation('text/plain')
    def post(self, login, group):
        """Adiciona usuario ao grupo"""
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
            return {
                "password": User(login).resetPassword(api.payload['password'])
            }
        except Exception as e:
            raise BadRequest(str(e))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
