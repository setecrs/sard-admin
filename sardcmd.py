#!/usr/bin/env python
import inspect
import cmd
import docopt

from pkg.operacao import Operacao
from pkg.usuario import Usuario

class Sard(cmd.Cmd):
    def do_operacao(self, line):
        """
Usage:
        operacao criacao OPERACAO
        operacao permissoes OPERACAO

"""
        try:
            args = docopt.docopt(self.do_operacao.__doc__, line.split(), help=False)
            operacao = Operacao(args['OPERACAO'])
            for x in 'criacao permissoes'.split():
                if args[x]:
                    f = Operacao.__dict__[x]
                    if inspect.isgeneratorfunction(f):
                        for x in f(operacao):
                            print x
                    else:
                        print f(operacao)
        except (docopt.DocoptExit) as e:
            print e


    def do_usuario(self, line):
        """
Usage:
        usuario criacao USUARIO
        usuario preenchimento USUARIO
        usuario permissoes USUARIO
        usuario listgroups USUARIO
        usuario zerar_senha USUARIO PWD
        usuario grupo USUARIO GRUPO

"""
        try:
            args = docopt.docopt(self.do_usuario.__doc__, line.split(), help=False)
            usuario = Usuario(args['USUARIO'], args)
            for x in 'criacao preenchimento permissoes listgroups zerar_senha grupo'.split():
                if args[x]:
                    if inspect.isgeneratorfunction(Usuario.__dict__[x]):
                        for x in Usuario.__dict__[x](usuario):
                            print x
                    else:
                        print Usuario.__dict__[x](usuario)
        except (docopt.DocoptExit) as e:
            print e

    def do_EOF(self, line):
        """quit"""
        return True
    do_quit = do_exit = do_EOF

    def postloop(self):
        print

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print Sard().onecmd(' '.join(sys.argv[1:]))
    else:
        Sard().cmdloop()
