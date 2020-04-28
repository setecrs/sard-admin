import os
import sys
import unittest
from subprocess import run

from pathlib import Path

sys.path.append(os.path.abspath('..'))
import sardadmin
import sardadmin.mock

groups = sardadmin.mock.Group.listAll()[:]
users = sardadmin.mock.User.listAll()[:]

if os.environ.get('TESTS') == 'SYSTEM':
    Group = sardadmin.group.Group
    User = sardadmin.user.User
    Auth = sardadmin.auth.Auth
    auth = Auth('JWT_SECRET', 'ldap')

    # extra measure to avoid running this in production
    assert set(groups) == set([x for x in Group.listAll() if x != 'testAdmin'])
    assert set(users) == set([x for x in User.listAll() if x != 'testAdmin'])

else:
    Group = sardadmin.mock.Group
    User = sardadmin.mock.User
    Auth = sardadmin.auth.Auth
    auth = Auth('JWT_SECRET', 'ldap', check_bind=lambda x, y, z: '')
    app = sardadmin._create_app(auth, User, Group)

def clean():
    for x in User.listAll():
        if not x in users:
            User(x).delete()
    for x in Group.listAll():
        if not x in groups:
            Group(x).delete()

class GroupTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        self.assertListEqual(Group.listAll(), groups)

    def test_criate_delete(self):
        self.assertListEqual(Group.listAll(), groups)
        Group('criate_delete', history_timeout=0.1).create()
        self.assertListEqual(Group.listAll(), groups + ['criate_delete'])
        Group('criate_delete').delete()
        self.assertListEqual(Group.listAll(), groups)

    def test_folder(self):
        if os.environ.get('TESTS') != 'SYSTEM':
            self.skipTest('env TESTS!=SYSTEM')
        Group('folder', history_timeout=1.0).create()
        self.assertListEqual(Group.listAll(), groups + ['folder'])
        Group.history[-1]['thread'].join()
        self.assertEqual(os.path.exists('/operacoes/folder'), True)
        stat = os.stat('/operacoes/folder')
        self.assertEqual(stat.st_mode, 0o40550)

    def test_users(self):
        Group('users', history_timeout=0.1).create()
        User('usersA').create()
        User('usersA').enterGroup('users')
        User('usersB').create()
        User('usersB').enterGroup('users')
        myusers = Group('users').users()
        self.assertListEqual(myusers, ['usersA', 'usersB'])

    def wait_history(self):
        while True:
            job = Group.history[-1]
            running = job['running']
            if not running:
                break
            job['thread'].join()

    def test_permissions(self, mode=0o000):
        if os.environ.get('TESTS') != 'SYSTEM':
            self.skipTest('env TESTS!=SYSTEM')
        if os.path.exists('/operacoes/permissions'):
            run(['rm', '-r', '/operacoes/permissions'], check=True)
        Group('permissions', history_timeout=0.1).create()
        self.wait_history()

        dirs = [
            '/operacoes/permissions/a/b/c',
        ]
        files = [
            '/operacoes/permissions/file.dd',
            '/operacoes/permissions/log',
            '/operacoes/permissions/SARD/Lista de Arquivos.csv',
            '/operacoes/permissions/SARD/indexador/somedir/java.jar',
        ]
        files2 = [
            '/operacoes/permissions/SARD/indexador/tools/file.txt',
            '/operacoes/permissions/SARD/indexador/jre/bin/file.txt',
            '/operacoes/permissions/SARD/indexador/lib/file.txt',
            '/operacoes/permissions/SARD/a.exe',
        ]
        uid = 0
        gid = Group('permissions').gid()
        for d in dirs:
            os.makedirs(d, mode=mode)
            os.chown(d, 13, 13)
        for f in files + files2:
            os.makedirs(os.path.dirname(f), mode=mode, exist_ok=True)
            Path(f).touch(mode=mode)
            os.chown(f, 13, 13)
        Group('permissions', history_timeout=0.1).permissions()
        self.wait_history()

        for d in dirs:
            self.assertEqual(os.stat(d).st_mode, 0o40555, d)
        for f in files:
            self.assertEqual(os.stat(f).st_mode, 0o100444, f)
        for d in [
            '/operacoes/permissions',
        ]:
            self.assertEqual(os.stat(d).st_gid, gid, d)
            self.assertEqual(os.stat(d).st_uid, uid, d)
            self.assertEqual(os.stat(d).st_mode, 0o40550, d)
        for f in files2:
            self.assertEqual(os.stat(f).st_mode, 0o100555, f)
