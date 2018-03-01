#!/usr/bin/env python
import os
import cmd
import docopt

from operacao import Operacao
from usuario import Usuario

def command(s, verbose=True):
    if verbose:
        print s
    return os.system(s)

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
                    print Operacao.__dict__[x](operacao)
        except (docopt.DocoptExit) as e:
            print e


    def do_usuario(self, line):
        """
Usage:
        usuario criacao USUARIO
        usuario preenchimento USUARIO
        usuario permissoes USUARIO
        usuario listgroups USUARIO
        usuario zerar_senha USUARIO
        usuario grupo USUARIO GRUPO

"""
        try:
            args = docopt.docopt(self.do_usuario.__doc__, line.split(), help=False)
            usuario = Usuario(args['USUARIO'], args)
            for x in 'criacao preenchimento permissoes listgroups zerar_senha grupo'.split():
                if args[x]:
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
        Sard().onecmd(' '.join(sys.argv[1:]))
    else:
        Sard().cmdloop()
