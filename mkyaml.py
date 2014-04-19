#!/usr/bin/python
import os,sys
import pytsk3
import yaml
import tempfile
from sardutils import *

def main(*dirs):
    if len(dirs)==0:
        cmd="ls -d */"
        dirs=os.popen(cmd).read().split('\n')
        dirs=[x.rstrip('/') for x in dirs if x and not x.startswith('20')]
    for d in dirs:
        new={}
        paths=[]
        print d
        for s in ['','pericia/','pericia/imagem/']:
            cmd='ls %s/*/%simagem.* 2>/dev/null'%(d,s)
            paths+=os.popen(cmd).read().split('\n')
        paths=[x for x in paths if x]
        tf=tempfile.mktemp()
        for path in paths:
            equipe,item=path.split('/',2)[0:2]
            if new and new.has_key(equipe) and new[equipe].has_key(item):
                pass
            else:
                dickey(new,equipe)
                dickey(new[equipe],item)
                cand=partinfo(path)
                new[equipe][item]=cand
        with open(tf,'w') as f:
            f.write(yaml.dump(new,default_flow_style=False))
        cmd='diff -a %s.yml %s || mv -i %s %s.yml'%(d,tf,tf,d)
        command(cmd,False)

def partinfo(imagepath):
  x=0
  y=0
  result=[]
  for particao in readpartitiontable3(imagepath):
      if particao['type'] in ['Safety Table', 
                              'Unallocated', 
                              'GPT Header', 
                              'Partition Table',
                              'Primary Table (#0)']:
          pass
      else:
          if (int(particao['size']) in [81920,
                                        1024000,
                                        204800,
                                        31457280] or 
              particao['type'] in ['EFI system partition',
                                  'Microsoft reserved partition',
                                  'Microsoft recovery partition']):
              dest='System'+str(y)
              y+=1
          else:
              dest=chr(ord('C')+x)
              x+=1
          result.append({'mnt':dest,
                         'offset':int(particao['offset']),
                         'path':imagepath,
                         })
  return result

def readpartitiontable3(ddfilepath):
  particoes=[]
  img=pytsk3.Img_Info(ddfilepath)
  try:
      volume = pytsk3.Volume_Info(img)
      for part in volume:
          if part.flags in [pytsk3.TSK_VS_PART_FLAG_ALLOC]:
              particoes.append({'offset':part.start*512,
                                'size':part.len,
                                'type':part.desc})
  except:
      particoes.append({'offset':0,
                        'size':img.get_size(),
                        'type':''})
      
  return particoes

if __name__=='__main__':
  main(*sys.argv[1:])

