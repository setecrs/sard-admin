import os, sys
import unittest
import requests
import time
from threading import Thread
from pathlib import Path
from grp import getgrnam
from subprocess import run
from pwd import getpwnam
from grp import getgrnam

sys.path.append(os.path.abspath('..'))

from pkg.operacao import Operacao, listgroups
from pkg.usuario import Usuario, listusers
import pkg.operacao

grupos = [
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

usuarios = [
    'root',
    'nobody',
]

def clean():
    run(['sss_cache', '-U', '-G'], check=True)
    for x in listusers():
        if not x in usuarios:
            Usuario(x).delete()
    for x in listgroups():
        if not x in grupos:
            Operacao(x).delete()    

# extra measure to avoid running this in production
assert set(grupos) == set(listgroups())

# extra measure to avoid running this in production
assert set(usuarios) == set(listusers())

class UsuarioTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        data = listusers()
        self.assertListEqual(data, usuarios)

    def test_criacao_delete(self):
        self.assertListEqual(listusers(), usuarios)
        Usuario('criacao_delete', history_timeout=0.1).criacao()
        self.assertListEqual(listusers(), usuarios + ['criacao_delete'])
        Usuario('criacao_delete').delete()
        self.assertListEqual(listusers(), usuarios)
        self.assertListEqual(listgroups(), grupos)
    
    def test_permissoes(self):
        mypath = '/home/permissoes/a/b/c/d/e/f'
        os.makedirs(mypath, mode=0o000)
        Usuario('permissoes', history_timeout=0.1).criacao()
        uid = getpwnam('permissoes').pw_uid
        gid = getgrnam('permissoes').gr_gid
        self.assertEqual(os.stat(mypath).st_gid, gid)
        self.assertEqual(os.stat(mypath).st_uid, uid)
        os.removedirs(mypath)

    def test_preenchimento(self):
        Usuario('preenchimento', history_timeout=0.1).criacao()
        rdp_path = f'/home/preenchimento/Desktop/SARD.rdp'
        rdp_path2 = f'/mnt/cloud/operacoes/Administrators/rdps/preenchimento/Desktop/SARD.rdp'
        rdp_path2_zip = os.path.dirname(rdp_path2) + f'preenchimento.zip'
        for x in [rdp_path, rdp_path2, rdp_path2_zip]:
            self.assertEqual(os.path.exists(x), True)


class OperacaoTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        data = listgroups()
        self.assertListEqual(data, grupos)

    def test_criacao_delete(self):
        self.assertListEqual(listgroups(), grupos)
        Operacao('criacao_delete', history_timeout=0.1).criacao()
        self.assertListEqual(listgroups(), grupos + ['criacao_delete'])
        Operacao('criacao_delete').delete()
        self.assertListEqual(listgroups(), grupos)

    def test_folder(self):
        Operacao('folder', history_timeout=0.1).criacao()
        self.assertListEqual(listgroups(), grupos + ['folder'])
        self.assertEqual(os.path.exists('/operacoes/folder'), True) 
        stat = os.stat('/operacoes/folder')
        self.assertEqual(stat.st_mode, 0o40750)

    def test_users(self):
        Operacao('users', history_timeout=0.1).criacao()
        Usuario('usersA', history_timeout=0.1).criacao()
        Usuario('usersA').grupo('users')
        Usuario('usersB', history_timeout=0.1).criacao()
        Usuario('usersB').grupo('users')
        users = Operacao('users').users()
        self.assertListEqual(users, ['usersA', 'usersB'])
    
    def wait_history(self):
        while True:
            job = pkg.operacao.history[-1]
            running = job['running']
            if not running:
                break

    def test_permissoes(self, mode=0o000):
        if os.path.exists('/operacoes/permissoes'):
            run(['rm', '-r', '/operacoes/permissoes'])
        Operacao('permissoes',history_timeout=0.1).criacao()
        self.wait_history()

        dirs = [
            '/operacoes/permissoes/a/b/c',
        ]
        files = [
            '/operacoes/permissoes/file.dd',
            '/operacoes/permissoes/log',
            '/operacoes/permissoes/SARD/Lista de Arquivos.csv',
            '/operacoes/permissoes/SARD/indexador/somedir/java.jar',
        ]
        files2 = [
            '/operacoes/permissoes/SARD/indexador/tools/file.txt',
            '/operacoes/permissoes/SARD/indexador/jre/bin/file.txt',
            '/operacoes/permissoes/SARD/indexador/lib/file.txt',
            '/operacoes/permissoes/SARD/a.exe',
        ]
        uid = 0
        gid = getgrnam('permissoes').gr_gid
        for d in dirs:
            os.makedirs(d, mode=mode)
            os.chown(d, 13, 13)
        for f in files + files2:        
            os.makedirs(os.path.dirname(f), mode=mode, exist_ok=True)
            Path(f).touch(mode=mode)
            os.chown(f, 13, 13)
        Operacao('permissoes', history_timeout=0.1).permissoes()
        self.wait_history()

        for d in dirs:
            self.assertEqual(os.stat(d).st_gid, gid, d)
            self.assertEqual(os.stat(d).st_uid, uid, d)
            self.assertEqual(os.stat(d).st_mode, 0o40555, d)
        for f in files:
            self.assertEqual(os.stat(f).st_mode, 0o100444, f)
            self.assertEqual(os.stat(f).st_uid, uid, f)
            self.assertEqual(os.stat(f).st_gid, gid, f)
        for d in [
            '/operacoes/permissoes',
        ]:
            self.assertEqual(os.stat(d).st_mode, 0o40750, d)
        for f in files2:
            self.assertEqual(os.stat(f).st_mode, 0o100555, f)
            self.assertEqual(os.stat(f).st_uid, uid, f)
            self.assertEqual(os.stat(f).st_gid, gid, f)

    def test_permissoesexe(self, mode=0o000):
        if os.path.exists('/operacoes/permissoesexe'):
            run(['rm', '-r', '/operacoes/permissoesexe'])
        Operacao('permissoesexe',history_timeout=0.1).criacao()
        self.wait_history()

        dirs = [
            '/operacoes/permissoesexe/a/b/c',
        ]
        files = [
            '/operacoes/permissoesexe/file.dd',
            '/operacoes/permissoesexe/log',
            '/operacoes/permissoesexe/SARD/Lista de Arquivos.csv',
            '/operacoes/permissoesexe/SARD/indexador/somedir/java.jar',
        ]
        files2 = [
            '/operacoes/permissoesexe/SARD/indexador/tools/file.txt',
            '/operacoes/permissoesexe/SARD/indexador/jre/bin/file.txt',
            '/operacoes/permissoesexe/SARD/indexador/lib/file.txt',
            '/operacoes/permissoesexe/SARD/a.exe',
        ]
        uid = 0
        gid = getgrnam('permissoesexe').gr_gid
        for d in dirs:
            os.makedirs(d, mode=mode)
            os.chown(d, 13, 13)
        for f in files + files2:        
            os.makedirs(os.path.dirname(f), mode=mode, exist_ok=True)
            Path(f).touch(mode=mode)
            os.chown(f, 13, 13)
        Operacao('permissoesexe',history_timeout=0.1).permissoesExe()
        self.wait_history()
        
        for d in dirs:
            self.assertEqual(os.stat(d).st_gid, 13, d)
            self.assertEqual(os.stat(d).st_uid, 13, d)
            self.assertEqual(os.stat(d).st_mode, 0o40000, d)
        for f in files:
            self.assertEqual(os.stat(f).st_mode, 0o100000, f)
            self.assertEqual(os.stat(f).st_uid, 13, f)
            self.assertEqual(os.stat(f).st_gid, 13, f)
        for d in [
            '/operacoes/permissoesexe',
        ]:
            self.assertEqual(os.stat(d).st_mode, 0o40750, d)
        for f in files2:
            self.assertEqual(os.stat(f).st_mode, 0o100111, f)
            self.assertEqual(os.stat(f).st_uid, 13, f)
            self.assertEqual(os.stat(f).st_gid, 13, f)

class APIGroupTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        resp = requests.get('http://api:5000/grupo/')
        data = resp.json()
        self.assertDictEqual(data, {"grupos": grupos})

    def test_add(self):
        resp = requests.post('http://api:5000/grupo/add')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/grupo/')
        data = resp.json()
        self.assertIn("add", data['grupos'])
        self.assertListEqual(listgroups(), grupos + ['add'])
        Operacao('add').delete()
        self.assertListEqual(listgroups(), grupos)

    def test_list_members(self):
        resp = requests.post('http://api:5000/grupo/list_members')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userAm')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userAm/grupo/list_members')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userBm')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userBm/grupo/list_members')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/grupo/list_members')
        data = resp.json()
        self.assertListEqual(data, ['userAm', 'userBm'])

    def test_double_add(self):
        resp = requests.post('http://api:5000/grupo/double_add')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/grupo/double_add')
        self.assertEqual(resp.ok, False)
    
    def test_double_perm(self):
        resp = requests.post('http://api:5000/grupo/double_perm')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/grupo/double_perm/permissoes')
        self.assertEqual(resp.ok, False)

    def test_double_perm_exe(self):
        resp = requests.post('http://api:5000/grupo/double_permexe')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/grupo/double_permexe/permissoesexe')
        self.assertEqual(resp.ok, False)

class APIUserTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_list(self):
        resp = requests.get('http://api:5000/usuario/')
        data = resp.json()
        self.assertDictEqual(data, {"usuarios": usuarios})

    def test_add(self):
        resp = requests.post('http://api:5000/usuario/addU')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/usuario/')
        data = resp.json()
        self.assertIn("addU", data['usuarios'])
        self.assertListEqual(listusers(), usuarios + ['addU'])
        Usuario('addU').delete()
        self.assertListEqual(listusers(), usuarios)
        self.assertListEqual(listgroups(), grupos)

    def test_add_listgroups(self):
        resp = requests.post('http://api:5000/grupo/groupA')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/grupo/groupB')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/grupo/groupC')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userList')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userList/grupo/groupA')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userList/grupo/groupB')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/userList/grupo/groupC')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.get('http://api:5000/usuario/userList')
        data = resp.json()
        self.assertListEqual(
            sorted(data['grupos']),
            sorted(['groupA', 'groupB', 'groupC', 'userList', 'Domain Users']))

    def test_double_add(self):
        resp = requests.post('http://api:5000/usuario/double_add')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/double_add')
        self.assertEqual(resp.ok, False)
    
class APIPasswordTest(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_change(self):
        resp = requests.post('http://api:5000/usuario/change')
        self.assertEqual(resp.text, "")
        self.assertEqual(resp.ok, True)
        resp = requests.post('http://api:5000/usuario/change/zerar_senha', json={
            "password": "1234"
        })
        self.assertDictEqual(resp.json(), {"senha": "1234"})
        self.assertEqual(resp.ok, True)
