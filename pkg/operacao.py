import os
import time

from command import command

def listgroups():
    return [x.split(':')[0] for x in os.popen('getent group').read().rstrip('\n').split('\n')]

class Operacao:
    def __init__(self, name):
        self.name = name

    def exists(self):
        return not os.system("getent group '%s'"%self.name)

    def ensure(self, tries=10):
        if not self.exists():
            if tries < 1:
                raise Exception('group doesn\'t exist')
            os.system('sss_cache -U -G')
            time.sleep(10)
            self.ensure(tries-1)


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
	    yield "Error making dir? Not a problem, let's move on.\n"
        for x in self.permissoes():
            yield x
    def permissoesExe(self):
        op = self.name
        for raw in command('find /operacoes/"%s" -name indexador -prune -o -name "?ista de ?rquivos.csv" -print '%(op)):
            for line in raw.strip().split('\n'):
		case = line.rsplit('/',1)[0]
                for subpath in ['*.exe', 'indexador/tools/', 'indexador/jre/bin/', 'indexador/lib/']:
                    for x in ignore(point(command))('chmod -cR a+x "%s"/"%s" '%(case, subpath)):
                        yield x
    def permissoes(self):
        self.ensure()
        op = self.name
        self.permissoesExe()
        for x in ignore(point(command))('chown -cR -h root:"%s" /operacoes/"%s"'%(op, op)):
            yield x
        for x in ignore(point(command))('chmod -c  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op)):
            yield x
        for x in ignore(point(command))('chmod -cR a+rX            /operacoes/"%s"/*'%(op)):
            yield x
        for x in ignore(point(command))('chmod -c  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op)):
            yield x
        yield "Ok"

def point(f):
  def handle(arg):
    first=True
    for x in f(arg):
      if first:
        first=False
        yield x
      else:
        yield "."
  return handle

def ignore(f):
  def handle(arg):
    try:
      for x in f(arg):
	yield x
    except Exception as e:
      yield "Ignoring error %s\n"%e.message
  return handle
