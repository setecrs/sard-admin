#!/usr/bin/python
import os
import sys
import yaml
import tempfile
import datetime
from sardutils import *
sys.path.insert(0,'/git/email')
import extracao_emails

def main(path,storage=None):
    with open(path) as f:
        equipes=yaml.load(f)
    for equipe,itens in equipes.iteritems():
        for item,parts in itens.iteritems():
            for part in parts:
                indir =SardPath(part['path']).getdir(dirtype='extracao',storage=storage)+'/'+part['mnt']
                outdir=SardPath(part['path']).getdir(dirtype='emails',storage=storage)+'/'+part['mnt']
                def functocall(outdirtemp):
                    dirmbox=outdirtemp+'-mbox'
                    dirmdir=outdirtemp
                    dirmdir=dirmdir.replace('/','\',1)
                    print '##################################'
                    command("date",False)
                    extracao_emails.main(mnt,dirmbox,dirmdir)
                    retiraacentos.retiraacentosdir(dirmdir)
                    return
                executeintemp(outdir,functocall)

main(*sys.argv[1:])
