#!/usr/bin/env python
import os
import cmd
import docopt
import yaml
import tempfile
import datetime
import random
from sardutils import *

# all_storages='vmhost1 vmhost2 vmhost3 storage1 backup1'.split()
all_storages='storage1 storage2 backup1'.split()

class Usuario:
    def __init__(self,name,args=None):
        self.name=name
        self.args=args
    def listgroups(self):
        return os.popen('groups '+self.name).read().rstrip('\n').split(' ')[2:]
    def criacao(self):
        u=self.name
        command('smbldap-groupadd -a "%s"'%u)
        print 'Sugestao de senha', random.randint(100000,999999)
        command('smbldap-useradd -a -g "%s" -P -s /bin/false -m  "%s"'%((u,)*2))
        command('smbldap-usermod --shadowMax 3650 "%s"'%u)
        self.grupo('Domain_Users')
        self.preenchimento()
    def preenchimento(self):
        u=self.name
        indices=''
        command('mkdir -p /home/%s/.maildir/operacoes'%u)
        command('echo > /home/%s/.maildir/operacoes/subscriptions'%u)
        command('mkdir -p -m 777 /home/%s/Desktop/operacoes/'%u)
        for g in self.listgroups():
            print "%s\t%s"%(u,g)
            command('ln -snf /sard/extracao/%s /home/%s/Desktop/operacoes/%s'%(g,u,g))
            if os.path.isdir('/sard/extracao/'+g):
                if not os.path.exists('/home/%s/ThunderbirdPortable'%u):
                    self.zerar_thunderbird()
                if os.path.exists('/storage1/mnt/config/subscriptions/%s.subscriptions'%g):
                    command('cat /storage1/mnt/config/subscriptions/%s.subscriptions >> /home/%s/.maildir/operacoes/subscriptions'%(g,u))
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
        self.permissoes()
    def grupo(self,grupo=None):
        u=self.name
        if grupo==None:
            grupo = self.args['GRUPO']
        command('smbldap-groupmod -m %s %s'%(u,grupo))
        command('sss_cache -U -G')
	self.preenchimento()
    def permissoes(self):
        command('chmod o-rwx -R /home/"%s" '%self.name)
        command('chown -h -R "%s":"%s" /home/"%s" '%((self.name,)*3))
    def zerar_thunderbird(self):
        u=self.name
        if os.path.exists('/home/%s/ThunderbirdPortable'%u):
            command("rm -r '/home/%s/ThunderbirdPortable'"%u)
        command('cp -r /git/sard-old/auxiliar/ThunderbirdPortable /home/%s/'%u)
        command("echo 'user_pref(\"mail.server.server2.userName\", \"%s\");' >> /home/%s/ThunderbirdPortable/Data/profile/prefs.js"%(u,u))
        command('chown -R %s:%s /home/%s/ThunderbirdPortable '%(u,u,u))
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
        for x in all_storages:
            command('mkdir /storages/%s/extracao/"%s"'%(x,op))
            command('mkdir /storages/%s/emails/"%s"'%(x,op))
            command('mkdir /storages/%s/imagens/"%s"'%(x,op))
        self.permissoes()
    def permissoes(self):
        op=self.name
        for x in all_storages:
            command('chown -R -h root:"%s" /storages/%s/extracao/"%s"'%(op,x,op))
            command('chown -R -h root:"%s" /storages/%s/emails/"%s"'%(op,x,op))
            command('chown -R -h root:"%s" /storages/%s/imagens/"%s"'%(op,x,op))
            command('chmod -R u=rX,g=rX,o-rwx /storages/%s/extracao/"%s"'%(x,op))
            command('chmod -R u=rX,g=rX,o-rwx /storages/%s/emails/"%s"'%(x,op))
            command('chmod -R u=rX,g=rX,o-rwx /storages/%s/imagens/"%s"'%(x,op))
# 05/05/2015 Aristeu: Adicionado suporte a criacao do diretorio de email da operacao e suas permissoes 
            
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
        usuario zerar_thunderbird USUARIO
        usuario zerar_senha USUARIO
        usuario grupo USUARIO GRUPO

"""
        try:
            args=docopt.docopt(self.do_usuario.__doc__,line.split(),help=False)
            usuario=Usuario(args['USUARIO'],args)
            for x in 'criacao preenchimento permissoes listgroups zerar_thunderbird zerar_senha grupo'.split():
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
    Sard().cmdloop()
