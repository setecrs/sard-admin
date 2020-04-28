import os
import sys
import unittest
import json

import requests

sys.path.append(os.path.abspath('..'))
import sardadmin
import sardadmin.mock

groups = sardadmin.mock.Group.listAll()[:]
users = sardadmin.mock.User.listAll()[:]

if os.environ.get('TESTS') == 'SYSTEM':
    prefix_url = 'http://api:80'
    Group = sardadmin.group.Group
    User = sardadmin.user.User
    Auth = sardadmin.auth.Auth
    auth = Auth('JWT_SECRET', 'ldap')

    # extra measure to avoid running this in production
    assert set(groups) == set([x for x in Group.listAll() if x != 'testAdmin'])

    # extra measure to avoid running this in production
    assert set(users) == set([x for x in User.listAll() if x != 'testAdmin'])

else:
    prefix_url = ''
    Group = sardadmin.mock.Group
    User = sardadmin.mock.User
    Auth = sardadmin.auth.Auth
    auth = Auth('JWT_SECRET', 'ldap', check_bind=lambda x, y, z: '')
    app = sardadmin._create_app(auth, User, Group)

    def to_requests(resp):
        r = lambda: None
        r.text = resp.data.decode('utf-8')
        r.status_code = resp.status_code
        r.ok = str(resp.status_code).startswith('2')
        r.json = lambda: json.loads(r.text)
        return r

    def get(*args, **kwargs):
        with app.test_client() as client:
            resp = client.get(*args, **kwargs)
            return to_requests(resp)

    def post(*args, **kwargs):
        with app.test_client() as client:
            resp = client.post(*args, **kwargs)
            return to_requests(resp)

    requests = lambda: None
    requests.get = get
    requests.post = post

if not 'testAdmin' in User.listAll():
    User('testAdmin').create()
User('testAdmin').resetPassword('testAdminPassword')
User('testAdmin').enterGroup('Domain Admins')
users.append('testAdmin')
groups.append('testAdmin')
resp = requests.post(prefix_url + '/auth/login', json=dict(
    user='testAdmin',
    password='testAdminPassword'
))
assert resp.ok
token = resp.json()['auth_token']

def clean():
    for x in User.listAll():
        if not x in users:
            User(x).delete()
    for x in Group.listAll():
        if not x in groups:
            Group(x).delete()

class APIGroupTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        resp = requests.get(prefix_url + '/group/')
        self.assertEqual(resp.ok, True)
        data = resp.json()
        self.assertDictEqual(data, {"groups": groups})

    def test_add_no_header(self):
        resp = requests.post(prefix_url + '/group/add')
        self.assertTrue(not 'add' in Group.listAll())
        self.assertEqual(resp.ok, False)

    def test_add(self):
        resp = requests.post(prefix_url + '/group/add', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get(prefix_url + '/group/')
        data = resp.json()
        self.assertIn("add", data['groups'])
        self.assertListEqual(Group.listAll(), groups + ['add'])

    def test_list_members(self):
        resp = requests.post(prefix_url + '/group/list_members', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userAm', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userAm/group/list_members', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userBm', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertTrue('password' in resp.json())
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userBm/group/list_members', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get(prefix_url + '/group/list_members')
        data = resp.json()
        self.assertDictEqual(data, dict(group='list_members', users=['userAm', 'userBm']))

    def test_double_add(self):
        resp = requests.post(prefix_url + '/group/double_add', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/group/double_add', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.ok, False)

    def test_double_perm(self):
        resp = requests.post(prefix_url + '/group/double_perm', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        for _ in range(5):
            resp = requests.post(prefix_url + '/group/double_perm/permissions', headers=dict(
                Authorization=f'Bearer {token}'
            ))
            if not resp.ok:
                return # we expect a not ok response eventually
        print(Group.history, file=sys.stderr)
        self.fail('multiple permissions call should fail')

    def test_perm_no_headers(self):
        resp = requests.post(prefix_url + '/group/Replicators/permissions')
        self.assertEqual(resp.ok, False)

class APIUserTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        resp = requests.get(prefix_url + '/user/')
        data = resp.json()
        self.assertDictEqual(data, {"users": users})

    def test_add_no_header(self):
        resp = requests.post(prefix_url + '/user/addU')
        self.assertTrue(not 'addU' in User.listAll())
        self.assertEqual(resp.ok, False)

    def test_add(self):
        resp = requests.post(prefix_url + '/user/addU', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertIsInstance(resp.json(), dict)
        self.assertTrue('password' in resp.json())
        self.assertEqual(resp.ok, True)
        resp = requests.get(prefix_url + '/user/')
        data = resp.json()
        self.assertIn("addU", data['users'])
        self.assertListEqual(User.listAll(), users + ['addU'])
        User('addU').delete()
        self.assertListEqual(User.listAll(), users)
        self.assertListEqual(Group.listAll(), groups)

    def test_add_group_no_headers(self):
        resp = requests.post(prefix_url + '/group/groupA1', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userA1', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.ok, True)
        self.assertTrue('password' in resp.json())
        resp = requests.post(prefix_url + '/user/userList/group/groupA')
        self.assertEqual(resp.ok, False)

    def test_add_listgroups(self):
        resp = requests.post(prefix_url + '/group/groupA', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/group/groupB', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/group/groupC', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userList', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertTrue('password' in resp.json())
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userList/group/groupA', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userList/group/groupB', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/userList/group/groupC', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get(prefix_url + '/user/userList')
        data = resp.json()
        expected = ['groupA', 'groupB', 'groupC', 'userList', 'Domain Users']
        for got in data['groups']:
            self.assertIn(got, expected)
        for e in expected:
            self.assertIn('userList', Group(e).users())

    def test_double_add(self):
        resp = requests.post(prefix_url + '/user/double_add2', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertTrue('password' in resp.json())
        self.assertEqual(resp.ok, True)
        resp = requests.post(prefix_url + '/user/double_add2', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.ok, False)

class APIPasswordTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_change(self):
        resp = requests.post(prefix_url + '/user/change', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.ok, True)
        self.assertTrue('password' in resp.json())
        resp = requests.post(prefix_url + '/user/change/reset_password', json={
            "password": "1234"
        }, headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertDictEqual(resp.json(), {"password": "1234"})
        self.assertEqual(resp.ok, True)

    def test_change_no_headers(self):
        resp = requests.post(prefix_url + '/user/change_no_header', headers=dict(
            Authorization=f'Bearer {token}'
        ))
        self.assertEqual(resp.ok, True)
        self.assertTrue('password' in resp.json())
        resp = requests.post(prefix_url + '/user/change_no_header/reset_password', json={
            "password": "1234"
        })
        self.assertEqual(resp.ok, False)
