#!/usr/bin/python
import sys
import yaml

def dickey(dic,key,list=False):
    if not dic.has_key(key):
        if list:
            dic[key]=[]
        else:
            dic[key]={}

def main(fstabpaths):
    result={}
    for path in fstabpaths:
        equipe,item=path.split('/')[-3:-1]
        dickey(result,equipe)
        dickey(result[equipe],item,list=True)
        with open(path) as f:
            for line in f:
                if line and line.strip() and not line.startswith('#'):
                    imagem,mnt,tipo,opts=line.split(' ')[:4]
                    x={}
                    x['path']=path.rsplit('/',1)[0]+'/'+imagem
                    x['mnt']=mnt
                    x['offset']=int(opts.split('offset=')[1].split(',')[0])
                    result[equipe][item].append(x)
    print yaml.dump(result,default_flow_style=False)

main(sys.argv[1:])
