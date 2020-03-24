import os
import random
import time
import zipfile
from subprocess import PIPE, STDOUT, run
from shutil import copyfile
from pwd import getpwnam
from grp import getgrnam

from .operacao import Operacao
from .mkrdp import mkrdp

def listusers():
    run(['sss_cache', '-U', '-G'], check=True)
    compl = run(['smbldap-userlist'], stdout=PIPE, encoding='utf-8', check=True)
    data = compl.stdout.split('\n')
    users = [x for x in data[1:] if '|' in x]
    users = [x.split('|')[1].strip() for x in users]
    return users

class Usuario:
    def __init__(self, name, args=None, history_timeout=3600):
        self.name = name
        self.args = args
        self.history_timeout = history_timeout

    def listgroups(self):
        run(['sss_cache', '-U', '-G'], check=True)
        proc = run(['id', '-Gnz', self.name], check=True, stdout=PIPE, encoding='utf-8')
        groups = proc.stdout.strip('\x00').split('\x00')
        return groups

    def exists(self):
        return self.name in listusers()

    def kill(self):
        proc = run(['smbstatus', '-bpu', self.name], stdout=PIPE, check=True, encoding='utf-8')
        lines = proc.stdout.strip().split('\n')
        for line in lines[1:]:
            pid = line.split(' ',1)[0]
            run(['kill', pid], check=True)

    def delete(self):
        run(['sss_cache', '-U', '-G'], check=True)
        run(['smbldap-userdel', self.name], check=True)
        run(['smbldap-groupdel', self.name], check=True)

    def criacao(self):
        run(['sss_cache', '-U', '-G'], check=True)
        if self.name in listusers():
            raise Exception('user already exists')
        run(['smbldap-groupadd', '-a', self.name], check=True)
        run(['smbldap-useradd', '-a', '-g', self.name, '-s', '/bin/false','-m', self.name], check=True)
        run(['sss_cache', '-U', '-G'], check=True)
        assert self.name in listusers()
        assert self.name in self.listgroups()
        self.grupo('Domain Users')
        self.preenchimento()
        return self.zerar_senha()

    def preenchimento(self):
        run(['sss_cache', '-U', '-G'], check=True)
        os.makedirs(f'/home/{self.name}/Desktop/operacoes', mode=0o777, exist_ok=True)
        mygroups = self.listgroups()
        mygroups.remove('Domain Users')
        for g in mygroups:
            if os.path.islink(f'/home/{self.name}/Desktop/operacoes'):
                break
            src = f'/mnt/cloud/operacoes/{g}'
            dst = f'/home/{self.name}/Desktop/operacoes/{g}'
            if not os.path.islink(dst):
                os.symlink(src, dst)
        with open(f'/home/{self.name}/Desktop/SARD.rdp', 'w', encoding='utf-8') as f:
            f.write(mkrdp(self.name))
        rdp_path = f'/home/{self.name}/Desktop/SARD.rdp'
        rdp_path2 = f'/mnt/cloud/operacoes/Administrators/rdps/{self.name}/Desktop/SARD.rdp'
        rdp_path2_zip = os.path.dirname(rdp_path2) + f'{self.name}.zip'
        os.makedirs(os.path.dirname(rdp_path2), exist_ok=True)
        copyfile(rdp_path, rdp_path2)
        with zipfile.ZipFile(rdp_path2_zip, 'w') as zipf:
            zipf.write(rdp_path, arcname='SARD.rdp')
        self.permissoes()

    def grupo(self, grupo=None):
        run(['sss_cache', '-U', '-G'], check=True)
        if grupo is None:
            grupo = self.args['GRUPO']
        op = Operacao(grupo)
        if not op.exists():
            raise Exception('Group doesn\'t exist')
        mygroups = self.listgroups()
        if grupo in mygroups:
            raise Exception(f'User {self.name} already in group {grupo}. Groups: {str(mygroups)}')
        run(['sss_cache', '-U', '-G'], check=True)
        run(['smbldap-groupmod', '-m', self.name, grupo], check=True)
        run(['sss_cache', '-U', '-G'], check=True)
        mygroups = self.listgroups()
        assert grupo in mygroups
        self.preenchimento()

    def permissoes(self):
        run(['sss_cache', '-U', '-G'], check=True)
        uid = getpwnam(self.name).pw_uid
        gid = getgrnam(self.name).gr_gid
        os.chmod(f'/home/{self.name}',0o700)
        for dirpath, dirnames, filenames in os.walk(f'/home/{self.name}', followlinks=False):
            for x in dirnames + filenames:
                fpath = os.path.join(dirpath, x)
                if not os.path.exists(fpath):
                    continue
                os.chown(fpath, uid, gid)

    def random_password(self):
        return str(random.randint(100000, 999999))

    def zerar_senha(self, password=None):
        run(['sss_cache', '-U', '-G'], check=True)
        if password in ["", "string", None]:
            password = self.random_password()
        run(['smbldap-passwd', '-p', self.name], check=True, input=password, encoding='utf-8')
        run(['smbldap-usermod', '--shadowMax', '3650', self.name], check=True)
        return {
            "senha": password
        }
