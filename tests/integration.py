import os
import sys
import unittest
from subprocess import run

from pathlib import Path
import requests

sys.path.append(os.path.abspath('..'))

from sardadmin.group import Group, history
from sardadmin.user import User

groups = [
    'Domain Admins',
    'Domain Users',
    'Domain Guests',
    'Domain Computers',
    'Administrators',
    'Account Operators',
    'Print Operators',
    'Backup Operators',
    'Replicators',
]

users = [
    'root',
    'nobody',
]

def clean():
    for x in User.listAll():
        if not x in users:
            User(x).delete()
    for x in Group.listAll():
        if not x in groups:
            Group(x).delete()    

# extra measure to avoid running this in production
assert set(groups) == set(Group.listAll())

# extra measure to avoid running this in production
assert set(users) == set(User.listAll())

class UserTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        self.assertListEqual(User.listAll(), users)

    def test_criate_delete(self):
        self.assertListEqual(User.listAll(), users)
        User('criate_delete').create()
        self.assertListEqual(User.listAll(), users + ['criate_delete'])
        User('criate_delete').delete()
        self.assertListEqual(User.listAll(), users)
        self.assertListEqual(Group.listAll(), groups)
    
    def test_permissions(self):
        mypath = '/home/permissions/a/b/c/d/e/f'
        os.makedirs(mypath, mode=0o000)
        User('permissions').create()
        uid = User('permissions').uid()
        gid = Group('permissions').gid()
        self.assertEqual(os.stat(mypath).st_gid, gid)
        self.assertEqual(os.stat(mypath).st_uid, uid)
        os.removedirs(mypath)

    def test_populateHome(self):
        User('populateHome').create()
        self.assertEqual(os.path.exists('/home/populateHome/Desktop/operacoes'), True)


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
        Group('folder', history_timeout=0.1).create()
        self.assertListEqual(Group.listAll(), groups + ['folder'])
        history[-1]['thread'].join()
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
            job = history[-1]
            running = job['running']
            if not running:
                break
            job['thread'].join()

    def test_permissions(self, mode=0o000):
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


class APIGroupTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        resp = requests.get('http://api:5000/group/')
        data = resp.json()
        self.assertDictEqual(data, {"groups": groups})

    def test_add(self):
        resp = requests.post('http://api:5000/group/add')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/group/')
        data = resp.json()
        self.assertIn("add", data['groups'])
        self.assertListEqual(Group.listAll(), groups + ['add'])
        Group('add').delete()
        self.assertListEqual(Group.listAll(), groups)

    def test_list_members(self):
        resp = requests.post('http://api:5000/group/list_members')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userAm')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userAm/group/list_members')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userBm')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userBm/group/list_members')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/group/list_members')
        data = resp.json()
        self.assertListEqual(data, ['userAm', 'userBm'])

    def test_double_add(self):
        resp = requests.post('http://api:5000/group/double_add')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/group/double_add')
        self.assertEqual(resp.ok, False)
    
    def test_double_perm(self):
        resp = requests.post('http://api:5000/group/double_perm')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/group/double_perm/permissions')
        self.assertEqual(resp.ok, False)

class APIUserTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        resp = requests.get('http://api:5000/user/')
        data = resp.json()
        self.assertDictEqual(data, {"users": users})

    def test_add(self):
        resp = requests.post('http://api:5000/user/addU')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/user/')
        data = resp.json()
        self.assertIn("addU", data['users'])
        self.assertListEqual(User.listAll(), users + ['addU'])
        User('addU').delete()
        self.assertListEqual(User.listAll(), users)
        self.assertListEqual(Group.listAll(), groups)

    def test_add_listgroups(self):
        resp = requests.post('http://api:5000/group/groupA')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/group/groupB')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/group/groupC')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userList')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userList/group/groupA')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userList/group/groupB')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/userList/group/groupC')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/user/userList')
        data = resp.json()
        self.assertListEqual(
            sorted(data['groups']),
            sorted(['groupA', 'groupB', 'groupC', 'userList', 'Domain Users']))

    def test_double_add(self):
        resp = requests.post('http://api:5000/user/double_add')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/double_add')
        self.assertEqual(resp.ok, False)
    
class APIPasswordTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_change(self):
        resp = requests.post('http://api:5000/user/change')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/user/change/reset_password', json={
            "password": "1234"
        })
        self.assertDictEqual(resp.json(), {"password": "1234"})
        self.assertEqual(resp.ok, True)
