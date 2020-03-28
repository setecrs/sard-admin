import os
import random
import time
import sys
from subprocess import PIPE, run

from .group import Group

def timeit(f):
    def g(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(end-start, 'User', f.__name__, file=sys.stderr)
        return result
    return g

class User:
    @staticmethod
    def listAll():
        "List all users in the LDAP database"
        compl = run(['smbldap-userlist'], stdout=PIPE, encoding='utf-8', check=True)
        lines = compl.stdout.strip().split('\n')
        lines = [x for x in lines[1:] if '|' in x]
        users = [x.split('|')[1].strip() for x in lines]
        return users

    def __init__(self, name):
        "Prepare a User instance, without touching the database"
        self.name = name

    @timeit
    def uid(self):
        "UID of user"
        proc = run(['smbldap-usershow', self.name], check=True, encoding='utf-8', stdout=PIPE)
        lines = proc.stdout.strip().split('\n')
        start = 'uidNumber: '
        for line in lines:
            if line.startswith(start):
                return int(line[len(start):])
        raise Exception(f'uid not found for {self.name}')

    @timeit
    def exists(self):
        "Returns whether the user exists in the LDAP database"
        return self.name in User.listAll()

    @timeit
    def groups(self):
        "List of groups of which user is a member"
        result = []
        for group in Group.listAll():
            if self.name in Group(group).users():
                result.append(group)
        return result

    @timeit
    def create(self, password=None):
        """Creates a new user, creates a group with the same name, 
        adds the user to the 'Domain Users' group, fill the home directory,
        and returns the new password."""
        if self.name in User.listAll():
            raise Exception('user already exists')
        run(['smbldap-groupadd', '-a', self.name], check=True)
        run(['smbldap-useradd', '-a', '-g', self.name, '-s', '/bin/false', '-m', self.name], check=True)
        self.enterGroup('Domain Users')
        self.populateHome()
        return self.resetPassword(password)

    @timeit
    def delete(self):
        "Delete user and the group with its name"
        run(['smbldap-userdel', self.name], check=True)
        run(['smbldap-groupdel', self.name], check=True)

    @timeit
    def enterGroup(self, group):
        "Adds the user to the group"
        op = Group(group)
        if not op.exists():
            raise Exception('Group does not exist')
        if not self.exists():
            raise Exception('User does not exist')
        run(['smbldap-groupmod', '-m', self.name, group], check=True)
        self.populateHome()

    @timeit
    def resetPassword(self, password=None):
        """Resets the user password.
        If the password is None or '', a random password is created.
        Returs the new password"""
        if password in ["", None]:
            password = random_password()
        run(['smbldap-passwd', '-p', self.name], check=True, input=password, encoding='utf-8')
        run(['smbldap-usermod', '--shadowMax', '3650', self.name], check=True)
        return password

    @timeit
    def permissions(self):
        "Adjusts the user's home permissions"
        uid = self.uid()
        gid = Group(self.name).gid()
        os.chmod(f'/home/{self.name}',0o700)
        for dirpath, dirnames, filenames in os.walk(f'/home/{self.name}', followlinks=False):
            for x in dirnames + filenames:
                fpath = os.path.join(dirpath, x)
                if not os.path.exists(fpath):
                    continue
                os.chown(fpath, uid, gid)

    @timeit
    def populateHome(self):
        "Populates the user's home directory with links to their groups"
        os.makedirs(f'/home/{self.name}/Desktop/operacoes', mode=0o777, exist_ok=True)
        mygroups = self.groups()
        mygroups.remove('Domain Users')
        for g in mygroups:
            if os.path.islink(f'/home/{self.name}/Desktop/operacoes'):
                break
            src = f'/mnt/cloud/operacoes/{g}'
            dst = f'/home/{self.name}/Desktop/operacoes/{g}'
            if not os.path.islink(dst):
                os.symlink(src, dst)
        self.permissions()

def random_password():
    "Returns a random password"
    return str(random.randint(100000, 999999))

