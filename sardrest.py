#!/usr/bin/env python

from flask import Flask, stream_with_context, Response
from flask_restplus import Resource, Api
from werkzeug.exceptions import BadRequest

from pkg.usuario import Usuario, listusers
from pkg.operacao import Operacao, listgroups

app = Flask(__name__)                  #  Create a Flask WSGI appliction
api = Api(app)                         #  Create a Flask-RESTPlus API

def respGen(generator):
    def g():
        try:
            for x in generator:
                yield x
        except (Exception) as e:
            yield str(e)
    return Response(stream_with_context(g()))

@api.route('/grupo/')
class GroupRoute(Resource):
    def get(self):
        try:
            groups = listgroups()
            return {
                'grupos': groups,
            }
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/grupo/<string:grupo>')
class GroupNewRoute(Resource):
    def get(self, grupo):
        try:
            group = Operacao(grupo)
            return group.users()
        except Exception as e:
            raise BadRequest(str(e))

    @api.representation('text/plain')
    def post(self, grupo):
        try:
            group = Operacao(grupo)
            return respGen(group.criacao())
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/grupo/<string:grupo>/permissoes')
class GroupPermsRoute(Resource):
    @api.representation('text/plain')
    def post(self, grupo):
        try:
            group = Operacao(grupo)
            return respGen(group.permissoes())
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario')
class UsuarioListRoute(Resource):
    def get(self):
        try:
            usuarios = listusers()
            return {
                'usuarios': usuarios,
            }
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/<string:login>')
class UsuarioCriacaoRoute(Resource):
    def get(self, login):
        try:
            usuario = Usuario(login)
            groups = usuario.listgroups()
            return {
                'usuario': login,
                'grupos': groups,
            }
        except Exception as e:
            raise BadRequest(str(e))
    @api.representation('text/plain')
    def post(self, login):
        try:
            usuario = Usuario(login)
            return respGen(usuario.criacao())
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/<string:login>/grupo/<string:grupo>')
class UsuarioGrupoRoute(Resource):
    @api.representation('text/plain')
    def post(self, login, grupo):
        try:
            usuario = Usuario(login)
            return respGen(usuario.grupo(grupo))
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/<string:login>/kill')
class UsuarioKillRoute(Resource):
    @api.representation('text/plain')
    def post(self, login):
        try:
            usuario = Usuario(login)
            return respGen(usuario.kill())
        except Exception as e:
            raise BadRequest(str(e))
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
