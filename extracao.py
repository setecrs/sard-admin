#!/usr/bin/python
import os
import sys
import yaml
import tempfile
import datetime
from sardutils import *

def main(path,storage=None):
    with open(path) as f:
        equipes=yaml.load(f)
    for equipe,itens in equipes.iteritems():
        for item,parts in itens.iteritems():
            for part in parts:
                outdir=SardPath(part['path']).getdir(dirtype='extracao',storage=storage)+'/'+part['mnt']
                def functocall(outdirtemp):
                    print '##################################'
                    command("date",False)
                    return command("time tsk_recover -a -o %i '%s' '%s'" %(part['offset']/512,part['path'],outdirtemp))
                executeintemp(outdir,functocall)

main(*sys.argv[1:])
