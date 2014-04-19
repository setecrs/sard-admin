#!/usr/bin/python
import os
import sys
import yaml
import subprocess
from sardutils import *

def runhashes(particoes,hashfilename):
    ret=0
    if not (os.path.exists(hashfilename) and os.stat(hashfilename).st_size>0):
        cmdlst=['/git/hash/gerasha256.sh']
        for particao in particoes:
            cmdlst += [particao]
        print ' '.join(cmdlst)
        with open(hashfilename,'w') as file:
            ret=subprocess.Popen(cmdlst,stdout=file).wait()
            assert(ret==0)
        ret=subprocess.Popen(['sort','-t','\n','-k1.67',hashfilename,'-o',hashfilename]).wait()
        assert(ret==0)
        if os.stat(hashfilename).st_size==0:
            os.remove(hashfilename)
    return ret

def aux(equipe,item,letras,storage):
    print equipe,item
    origdir=os.path.realpath(os.curdir)
    itempath='%s/%s'%(equipe,item)
    filesdir =SardPath(itempath).getpath(dirtype='extracao',storage=storage)
    hashesdir=SardPath(itempath).getpath(dirtype='hashes',storage=storage)
    def functocall(tempdir):
        os.chdir(filesdir)
        outfile=tempdir +'/hashes.sha256'
        return runhashes(letras,outfile)
    executeintemp(hashesdir,functocall)
    os.chdir(origdir)

def main(path,storage=None):
    path=path.rstrip('/')
    if os.path.isdir(path):
        dirs=os.popen('ls -d %s/*/'%path).read().rstrip().split('\n')
        for d in dirs:
            equipe,item,rest=d.split('/',2)
            letras=os.popen('ls %s/%s'%(equipe,item)).read().rstrip().split('\n')
            aux(equipe,item,letras,storage)
    else:
        with open(path) as f:
            equipes=yaml.load(f)
        for equipe,itens in equipes.iteritems():
            for item,parts in itens.iteritems():
                aux(equipe,item,[x['mnt'] for x in parts],storage)

if __name__ == "__main__":
    main(*sys.argv[1:]) #main(operacao.yml)
