import os
from subprocess import run, PIPE

from .job import addJob

class Group:
    jobs = {}
    history = []

    @staticmethod
    def listAll():
        "List all groups in the LDAP database"
        proc = run(['smbldap-grouplist'], stdout=PIPE, encoding='utf-8', check=True)
        lines = proc.stdout.strip().split('\n')
        lines = [x for x in lines[1:] if '|' in x]
        groups = [x.split('|')[1].strip() for x in lines]
        return groups

    def __init__(self, name, history_timeout=3600):
        """Prepare a Group instance, without touching the database.
        history_timeout is for the permissions job,
                        it sets how long the job's output remains in history"""
        self.name = name
        self.history_timeout = history_timeout

    def gid(self):
        "GID of the group"
        proc = run(['smbldap-groupshow', self.name], check=True, encoding='utf-8', stdout=PIPE)
        lines = proc.stdout.strip().split('\n')
        start = 'gidNumber: '
        for line in lines:
            if line.startswith(start):
                return int(line[len(start):])
        raise Exception(f'gid not found for {self.name}')

    def exists(self):
        "Returns whether the group exists in the LDAP database"
        return self.name in Group.listAll()

    def users(self):
        "List the members of the group"
        proc = run(['smbldap-groupshow', self.name], stdout=PIPE, encoding='utf-8', check=True)
        lines = proc.stdout.strip().split('\n')
        start = 'memberUid: '
        users = []
        for x in lines:
            if x.startswith(start):
                x = x[len(start):]
                users += [x.strip() for x in x.split(',')]
        return users

    def create(self):
        """Creates a new group and creates the group folder."""
        if self.exists():
            raise Exception('Group already exists')
        op = self.name
        compl = run(['smbldap-groupadd', '-a', op], stdout=PIPE, check=True)
        os.makedirs(f'/operacoes/{op}', mode=0o770, exist_ok=True)
        self.permissions()

    def delete(self):
        "Deletes the group"
        if self.name in Group.jobs:
            Group.jobs[self.name]['thread'].join()
        run(['smbldap-groupdel', self.name], check=True)

    def permissions(self):
        """Adjusts the group folder permissions.
        The main group folder is only accessible by group members.
        Inner folders are always readable and executable.
        Inner files are always readable. Some are executable too."""
        group_root = '/operacoes'
        def f():
            gid = self.gid()
            myroot = os.path.join(group_root, self.name)
            #The main group folder is only accessible by group members.
            os.chown(myroot, 0, gid, follow_symlinks=False)
            os.chmod(myroot, 0o070)
            for dirpath, dirnames, filenames in os.walk(myroot):
                for x in dirnames:
                    #Inner folders are always readable and executable.
                    xpath = os.path.join(dirpath, x)
                    oldmode = os.stat(xpath, follow_symlinks=False).st_mode
                    oldmode = oldmode & 0o777 # consider only lower bits
                    newmode = oldmode
                    newmode = newmode | 0o444 # everybody can read
                    newmode = newmode | 0o111 # everybody can execute
                    if oldmode != newmode:
                        os.chmod(xpath, newmode)
                        Group.jobs[self.name]['output'] += f'oldmode: {oct(oldmode)} newmode: {oct(newmode)} path: {xpath}\n'
                for x in filenames:
                    #Inner files are always readable. Some are executable too.
                    xpath = os.path.join(dirpath, x)
                    oldmode = os.stat(xpath, follow_symlinks=False).st_mode
                    oldmode = oldmode & 0o777 # consider only lower bits
                    newmode = oldmode
                    newmode = newmode | 0o444 # everybody can read
                    if  ('indexador/tools' in dirpath or
                         'indexador/jre/bin' in dirpath or
                         'indexador/lib' in dirpath or
                         x.endswith('.exe')):
                        newmode = newmode | 0o111 # everybody can execute
                    if oldmode != newmode:
                        os.chmod(xpath, newmode)
                        Group.jobs[self.name]['output'] += f'oldmode: {oct(oldmode)} newmode: {oct(newmode)} path: {xpath}\n'
        addJob(Group.jobs, self.name, Group.history, f, self.history_timeout)
