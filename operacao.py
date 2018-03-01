import os

def command(s, verbose=True):
    if verbose:
        print s
    return os.system(s)

class Operacao:
    def __init__(self, name):
        self.name = name
    def criacao(self):
        op = self.name
        command('smbldap-groupadd "%s"'%op)
        command('mkdir /operacoes/"%s"'%(op))
        self.permissoes()
    def permissoes(self):
        op = self.name
        command('find /operacoes/"%s" -name indexador -prune -o -name "Ferramenta de Pesquisa.exe" -print0 | xargs -L1 -0 chmod -v a+x '%(op))
        command('find /operacoes/"%s" -name indexador -prune -o -name "IPED-SearchApp.exe" -print0 | xargs -L1 -0 chmod -v a+x '%(op))
        command('chown -vR -h root:"%s" /operacoes/"%s"'%(op, op))
        command('chmod -v  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op))
        command('chmod -vR a+rX            /operacoes/"%s"/*'%(op))
        command('chmod -v  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op))
