#!/usr/bin/env python

from flask import Flask
from flask_restplus import Resource, Api
from werkzeug.exceptions import BadRequest

from usuario import Usuario

app = Flask(__name__)                  #  Create a Flask WSGI appliction
api = Api(app)                         #  Create a Flask-RESTPlus API

# class ErrorHandler(Exception):
#     status_code = 400
#
#     def __init__(self, message, status_code=None, payload=None):
#         Exception.__init__(self)
#         self.message = message
#         if status_code is not None:
#             self.status_code = status_code
#         self.payload = payload
#
#     def to_dict(self):
#         rv = dict(self.payload or ())
#         rv['message'] = self.message
#         return rv
#
# @app.errorhandler(ErrorHandler)
# def error_handler(error):
#     response = str(error)
#     response.status_code = error.status_code
#     return response

@api.route('/usuario/criacao/<string:login>')                   #  Create a URL route to this resource
class UsuarioRoute(Resource):            #  Create a RESTful resource
    def post(self, login):                     #  Create GET endpoint
        try:
            usuario = Usuario(login)
            senha = usuario.criacao()
            return {
                'usuario': login,
                'senha': senha,
            }
        except Exception as e:
            raise BadRequest(str(e))

if __name__ == '__main__':
    app.run(debug=True)                #  Start a development server
