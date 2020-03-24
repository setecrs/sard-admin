#!/usr/bin/env python3

from flask import Flask, stream_with_context, Response, make_response
from flask_restplus import Resource, Api, fields
from werkzeug.exceptions import BadRequest

from pkg.usuario import Usuario, listusers
from pkg.operacao import Operacao, listgroups, jobs, history

app = Flask(__name__)                  #  Create a Flask WSGI appliction
api = Api(app, default_mediatype='text/plain')                         #  Create a Flask-RESTPlus API

@api.route('/jobs/', methods=['GET'])
class Jobs(Resource):
    def get(self):
        return {
            "history": [dict((k,h[k]) for k in h if k != 'thread') for h in history],
            "jobs": dict([(op, dict((k,jobs[op][k]) for k in jobs[op] if k != 'thread')) for op in jobs]),
            }

@api.route('/grupo/')
class GroupRoute(Resource):
    def get(self):
        """Lista todos os grupos"""
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
        """Lista membros do grupo"""
        try:
            group = Operacao(grupo)
            return group.users()
        except Exception as e:
            raise BadRequest(str(e))

    @api.representation('text/plain')
    def post(self, grupo):
        """Cria novo grupo"""
        try:
            group = Operacao(grupo)
            group.criacao()
            return make_response('', 204)
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/grupo/<string:grupo>/permissoesexe')
class GroupPermsExeRoute(Resource):
    @api.representation('text/plain')
    def post(self, grupo):
        """Verifica e corrige permissoes do grupo"""
        try:
            group = Operacao(grupo)
            return group.permissoesExe()
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/grupo/<string:grupo>/permissoes')
class GroupPermsRoute(Resource):
    @api.representation('text/plain')
    def post(self, grupo):
        """Verifica e corrige permissoes do grupo"""
        try:
            group = Operacao(grupo)
            return group.permissoes()
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/')
class UsuarioListRoute(Resource):
    def get(self):
        """Lista todos os usuarios"""
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
        """Lista grupos do usuario"""
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
        """Cria novo usuario"""
        try:
            usuario = Usuario(login)
            usuario.criacao()
            return make_response('', 204)
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/<string:login>/grupo/<string:grupo>')
class UsuarioGrupoRoute(Resource):
    @api.representation('text/plain')
    def post(self, login, grupo):
        """Adiciona usuario ao grupo"""
        try:
            usuario = Usuario(login)
            usuario.grupo(grupo)
            return make_response('', 204)
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/<string:login>/preenchimento')
class UsuarioPreenchimentoRoute(Resource):
    @api.representation('text/plain')
    def post(self, login):
        """Verifica e corrige pasta home do usuario"""
        try:
            usuario = Usuario(login)
            usuario.preenchimento()
            return make_response('', 204)
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/<string:login>/permissoes')
class UsuarioPermsRoute(Resource):
    @api.representation('text/plain')
    def post(self, login):
        """Verifica e corrige permissoes do usuario"""
        try:
            usuario = Usuario(login)
            usuario.permissoes()
            return make_response('', 204)
        except Exception as e:
            raise BadRequest(str(e))

@api.route('/usuario/<string:login>/zerar_senha')
class UsuarioSenhaRoute(Resource):
    @api.representation('text/plain')
    @api.expect(api.model('data', {
        "password": fields.String(required=False, description='password'),
    }))
    def post(self, login):
        """Altera a senha do usuario. Se a senha for "" ou "string", uma senha aleatoria sera criada."""
        try:
            usuario = Usuario(login)
            return usuario.zerar_senha(api.payload['password'])
        except Exception as e:
            raise BadRequest(str(e))

# @api.route('/usuario/<string:login>/kill')
# class UsuarioKillRoute(Resource):
#     @api.representation('text/plain')
#     def post(self, login):
#         """Mata processo do usuario no samba - nao funciona pq samba esta em PID namespace diferente"""
#         try:
#             usuario = Usuario(login)
#             return respGen(usuario.kill())
#         except Exception as e:
#             raise BadRequest(str(e))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
