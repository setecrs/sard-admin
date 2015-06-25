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
                    print '##################################'
                    command("date",False)
                    extracao_emails.main(indir,dirmbox,dirmdir)
                    return 0
                executeintemp(outdir,functocall)

for x in sys.argv[1:]:
    main(x)
