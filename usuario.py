import os
import random
import zipfile

from mkrdp import mkrdp

def command(s, verbose=True):
    if verbose:
        print s
    return os.system(s)

class Usuario:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args

    def listgroups(self):
        return os.popen('groups '+self.name).read().rstrip('\n').split(' ')[2:]

    def criacao(self):
        u = self.name
        senha = random.randint(100000, 999999)
        print 'Senha inicial:', senha
        if command('smbldap-groupadd -a "%s"'%u): #if exit code not zero
            return 'refusing to proceed'
        command('smbldap-useradd -a -g "%s" -s /bin/false -m "%s"'%(u, u))
        command('smbldap-usermod --shadowMax 3650 "%s"'%u)
        command('echo "%s" | smbldap-passwd -p "%s"'%(senha, u))
        self.grupo('Domain Users')
        self.preenchimento()
    def preenchimento(self):
        u = self.name
        command('mkdir -p -m 777 /home/%s/Desktop/operacoes/'%u)
        for g in self.listgroups():
            print "%s\t%s"%(u, g)
            command('ln -snf /mnt/cloud/operacoes/%s /home/%s/Desktop/operacoes/%s'%(g, u, g))
        with open('/home/%s/Desktop/SARD.rdp'%u, 'w') as f:
            f.write(mkrdp(u))
        command("(cd /home; tar c */Desktop/SARD.rdp --mode='a+r' ) | tar x -C /mnt/cloud/operacoes/Administrators/rdps/")
        with zipfile.ZipFile('/mnt/cloud/operacoes/Administrators/rdps/%s/Desktop/SARD.zip'%u, 'w') as zipf:
            zipf.write('/mnt/cloud/operacoes/Administrators/rdps/%s/Desktop/SARD.rdp'%u, arcname='SARD.rdp')
        self.permissoes()
    def grupo(self, grupo=None):
        u = self.name
        if grupo is None:
            grupo = self.args['GRUPO']
        command("smbldap-groupmod -m %s '%s'"%(u, grupo))
        if command('sss_cache -U -G'):
            #if can not reset cache, wait a minute to refresh
            command('sleep 60')
        self.preenchimento()
    def permissoes(self):
        command('chmod o-rwx /home/"%s" '%self.name)
        command('chown -h -R "%s":"%s" /home/"%s" '%((self.name,)*3))
    def zerar_senha(self):
        u = self.name
        print 'Sugestao de senha', random.randint(100000, 999999)
        command('smbldap-passwd "%s"'%u)
        command('smbldap-usermod --shadowMax 3650 "%s"'%u)
