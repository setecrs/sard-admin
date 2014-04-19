#!/usr/bin/python
import os,sys
import datetime
                                        
def dickey(dic,key,list=False):
    if not dic.has_key(key):
        if list:
            dic[key]=[]
        else:
            dic[key]={}

def command(s,verbose=True):
    if verbose:
        print s
    return os.system(s)

def ask(question):
    resp='-'
    while not resp in 'SYN':
        resp=raw_input(question).strip().upper()
    return not resp=='N'

def executeintemp(destdir,functocall,skipexisting=True,interactive=True):
    if skipexisting and os.path.exists(destdir):
        print 'skiping:',destdir
    else:
        spath=SardPath(destdir)
        data=datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        tempdir=spath.getpath(dirtype='temp')+'-'+data
        command("mkdir -p '%s'"%spath.getdir(dirtype='temp'),False)
        os.mkdir(tempdir,0755)
        ret=functocall(tempdir)
        if interactive and ret!=0:
            print 'Erro. Comando retornou',ret
            if not ask('Deseja continuar?'):
                sys.exit(ret)
        else:
            command("mkdir -p '%s'"%spath.getdir(),False)
            command("mv -i '%s' '%s'"%(tempdir,destdir))
        return ret

class SardPath():
    def __init__(self,path):
        origpath=os.path.realpath(path)
        assert origpath.startswith('/storages/')
        self.prefix,self.storage,self.dirtype,self.relpath=origpath.lstrip('/').split('/',3)
    def getpath(self,storage=None,dirtype=None):
        storage=storage or self.storage
        dirtype=dirtype or self.dirtype
        return '/'+'/'.join([self.prefix,storage,dirtype,self.relpath])
    def getdir(self,storage=None,dirtype=None):
        return os.path.dirname(self.getpath(storage,dirtype))
