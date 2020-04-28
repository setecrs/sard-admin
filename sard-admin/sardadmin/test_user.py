import os
import sys
import unittest

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
    auth = Auth('JWT_SECRET', 'ldap', check_bind=lambda x,y,z:'')
    app = sardadmin._create_app(auth, User, Group)

def clean():
    for x in User.listAll():
        if not x in users:
            User(x).delete()
    for x in Group.listAll():
        if not x in groups:
            Group(x).delete()

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
        if os.environ.get('TESTS') != 'SYSTEM':
            self.skipTest('env TESTS!=SYSTEM')
        mypath = '/home/permissions/a/b/c/d/e/f'
        os.makedirs(mypath, mode=0o000)
        User('permissions').create()
        uid = User('permissions').uid()
        gid = Group('permissions').gid()
        self.assertEqual(os.stat(mypath).st_gid, gid)
        self.assertEqual(os.stat(mypath).st_uid, uid)
        os.removedirs(mypath)

    def test_populateHome(self):
        if os.environ.get('TESTS') != 'SYSTEM':
            self.skipTest('env TESTS!=SYSTEM')
        User('populateHome').create()
        self.assertEqual(os.path.exists('/home/populateHome/Desktop/operacoes'), True)
