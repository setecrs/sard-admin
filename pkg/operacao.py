import os
import subprocess

from command import command

def listgroups():
    return [x.split(':')[0] for x in os.popen('getent group').read().rstrip('\n').split('\n')]

class Operacao:
    def __init__(self, name):
        self.name = name

    def exists(self):
        return self.name in listgroups()

    def users(self):
        return [x for x in os.popen('getent group %s'%self.name).read().rstrip('\n').split(':')[-1].split(',')]

    def criacao(self):
        if self.exists():
            raise Exception('Group already exists')
        op = self.name
        for x in command('smbldap-groupadd "%s"'%op):
            yield x
        try:
            for x in command('mkdir /operacoes/"%s"'%(op)):
                yield x
        except:
            pass
        for x in self.permissoes():
            yield x
    def permissoes(self):
        if not self.exists():
            raise Exception('Group doesn\'t exist')
        op = self.name
        for x in command('find /operacoes/"%s" -name indexador -prune -o -name "Ferramenta de Pesquisa.exe" -print0 -o -name "IPED-SearchApp.exe" -print0 | xargs -L1 -0 chmod -v a+x '%(op)):
            yield x
        for x in command('chown -vR -h root:"%s" /operacoes/"%s"'%(op, op)):
            yield x
        for x in command('chmod -v  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op)):
            yield x
        for x in command('chmod -vR a+rX            /operacoes/"%s"/*'%(op)):
            yield x
        for x in command('chmod -v  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op)):
            yield x
