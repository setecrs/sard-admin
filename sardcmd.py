#!/usr/bin/env python
import os
import cmd
import docopt
import tempfile
import datetime
import random
import zipfile

def command(s,verbose=True):
    if verbose:
        print s
    return os.system(s)

class Usuario:
    def __init__(self,name,args=None):
        self.name=name
        self.args=args
    def listgroups(self):
        return os.popen('groups '+self.name).read().rstrip('\n').split(' ')[2:]
    def criacao(self):
        u=self.name
	senha = random.randint(100000,999999)
        print 'Senha inicial:', senha
        if command('smbldap-groupadd -a "%s"'%u): #if exit code not zero
            return 'refusing to proceed'
        command('smbldap-useradd -a -g "%s" -s /bin/false -m "%s"'%(u,u))
        command('smbldap-usermod --shadowMax 3650 "%s"'%u)
	command('echo "%s" | smbldap-passwd -p "%s"'%(senha,u))
        self.grupo('Domain Users')
        self.preenchimento()
    def preenchimento(self):
        u=self.name
        indices=''
        command('mkdir -p -m 777 /home/%s/Desktop/operacoes/'%u)
        for g in self.listgroups():
            print "%s\t%s"%(u,g)
            command('ln -snf /mnt/cloud/operacoes/%s /home/%s/Desktop/operacoes/%s'%(g,u,g))
        with open('/home/%s/Desktop/SARD.rdp'%u,'w') as f:
            f.write("""screen mode id:i:2
use multimon:i:0
desktopwidth:i:800
desktopheight:i:600
session bpp:i:32
winposstr:s:0,3,0,0,800,600
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:2
displayconnectionbar:i:1
disable wallpaper:i:1
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:10.51.4.190
audiomode:i:0
redirectprinters:i:1
redirectcomports:i:0
redirectsmartcards:i:1
redirectclipboard:i:1
redirectposdevices:i:0
redirectdirectx:i:1
autoreconnection enabled:i:1
authentication level:i:2
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:1
use redirection server name:i:0
username:s:SARD\%s
"""%u)
        command("(cd /home; tar c */Desktop/SARD.rdp --mode='a+r' ) | tar x -C /mnt/cloud/operacoes/Administrators/rdps/")
        with zipfile.ZipFile('/mnt/cloud/operacoes/Administrators/rdps/%s/Desktop/SARD.zip'%u,'w') as zipf:
          zipf.write('/mnt/cloud/operacoes/Administrators/rdps/%s/Desktop/SARD.rdp'%u, arcname='SARD.rdp')
        self.permissoes()
    def grupo(self,grupo=None):
        u=self.name
        if grupo==None:
            grupo = self.args['GRUPO']
        command("smbldap-groupmod -m %s '%s'"%(u,grupo))
        if command('sss_cache -U -G'):
            #if can not reset cache, wait a minute to refresh
            command('sleep 60') 
	self.preenchimento()
    def permissoes(self):
        command('chmod o-rwx /home/"%s" '%self.name)
        command('chown -h -R "%s":"%s" /home/"%s" '%((self.name,)*3))
    def zerar_senha(self):
        u=self.name
        print 'Sugestao de senha', random.randint(100000,999999)
        command('smbldap-passwd "%s"'%u)
        command('smbldap-usermod --shadowMax 3650 "%s"'%u)
        

class Operacao:
    def __init__(self,name):
        self.name=name
    def criacao(self):
        op=self.name
        command('smbldap-groupadd "%s"'%op)
        command('mkdir /operacoes/"%s"'%(op))
        self.permissoes()
    def permissoes(self):
        op=self.name
        command('find /operacoes/"%s" -name indexador -prune -o -name "Ferramenta de Pesquisa.exe" -print0 | xargs -L1 -0 chmod -v a+x '%(op))
        command('find /operacoes/"%s" -name indexador -prune -o -name "IPED-SearchApp.exe" -print0 | xargs -L1 -0 chmod -v a+x '%(op))
        command('chown -vR -h root:"%s" /operacoes/"%s"'%(op,op))
        command('chmod -v  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op))
        command('chmod -vR a+rX            /operacoes/"%s"/*'%(op))
        command('chmod -v  u+rX,g+rX,o-rwx /operacoes/"%s"'%(op))
            
class Sard(cmd.Cmd):
    def do_operacao(self,line):
        """
Usage:
        operacao criacao OPERACAO
        operacao permissoes OPERACAO

"""
        try:
            args=docopt.docopt(self.do_operacao.__doc__,line.split(),help=False)
            operacao=Operacao(args['OPERACAO'])
            for x in 'criacao permissoes'.split():
                if args[x]:
                    print Operacao.__dict__[x](operacao)
        except (docopt.DocoptExit) as e:
            print e
    
    
    def do_usuario(self,line):
        """
Usage:
        usuario criacao USUARIO
        usuario preenchimento USUARIO
        usuario permissoes USUARIO
        usuario listgroups USUARIO
        usuario zerar_senha USUARIO
        usuario grupo USUARIO GRUPO

"""
        try:
            args=docopt.docopt(self.do_usuario.__doc__,line.split(),help=False)
            usuario=Usuario(args['USUARIO'],args)
            for x in 'criacao preenchimento permissoes listgroups zerar_senha grupo'.split():
                if args[x]:
                    print Usuario.__dict__[x](usuario)
        except (docopt.DocoptExit) as e:
            print e

    def do_EOF(self, line):
        """quit"""
        return True
    do_quit=do_exit=do_EOF

    def postloop(self):
        print

if __name__=='__main__':
    import sys
    if len(sys.argv)>1:
        Sard().onecmd(' '.join(sys.argv[1:]))
    else:
        Sard().cmdloop()
