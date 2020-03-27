import os
import time
from subprocess import run, PIPE, STDOUT
import subprocess
from threading import Thread

from .command import command
from .job import addJob

jobs = {}
history = []

def listgroups():
    proc = run(['smbldap-grouplist'], stdout=PIPE, encoding='utf-8', check=True)
    data = proc.stdout.strip().split('\n')
    groups = [x for x in data[1:] if '|' in x]
    groups = [x.split('|')[1].strip() for x in groups]
    return groups

class Operacao:
    def __init__(self, name, history_timeout=3600):
        self.name = name
        self.history_timeout = history_timeout

    def exists(self):
        return self.name in listgroups()

    def users(self):
        proc = run(['smbldap-groupshow', self.name], stdout=PIPE, encoding='utf-8', check=True)
        data = proc.stdout.strip().split('\n')
        start = 'memberUid: '
        users = []
        for x in data:
            if x.startswith(start):
                x = x[len(start):]
                users += [x.strip() for x in x.split(',')]
        return users

    def criacao(self):
        if self.exists():
            raise Exception('Group already exists')
        op = self.name
        compl = run(['smbldap-groupadd', '-a', op], stdout=PIPE, check=True)
        run(['sss_cache', '-U', '-G'], check=True)
        os.makedirs(f'/operacoes/{op}' , mode=0o770, exist_ok=True)
        self.permissoes()

    def delete(self):
        if self.name in jobs:
            jobs[self.name]['thread'].join()
        compl = run(['smbldap-groupdel', self.name], check=True)
        run(['sss_cache', '-U', '-G'], check=True)

    def permissoes(self, full=True):
        if self.name in jobs:
            raise Exception('Another permission job is already running')
        run(['sss_cache', '-U', '-G'], check=True)
        op = self.name
        def f():
            if full:
                cmd = ['chown', '-cR', '-h', f'root:{op}', f'/operacoes/{op}']
                proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
                jobs[op]['output'] += proc.stdout

                cmd = ['chmod', '-c', 'u+rX,g+rX,o-rwx', f'/operacoes/{op}']
                proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
                jobs[op]['output'] += proc.stdout
                
                cmd = ['chmod', '-cR', 'a+rX', f'/operacoes/{op}']
                proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
                jobs[op]['output'] += proc.stdout
                
                cmd = ['chmod', '-c', 'u+rX,g+rX,o-rwx', f'/operacoes/{op}']
                proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
                jobs[op]['output'] += proc.stdout
            
            for dirpath, dirnames, filenames in os.walk(f'/operacoes/{op}'):
                if 'indexador' in dirnames:
                    dirnames.pop(dirnames.index('indexador'))
                if 'Lista de Arquivos.csv' in filenames:
                    files = [
                        'indexador/tools/',
                        'indexador/jre/bin/',
                        'indexador/lib/',
                    ]
                    for f in filenames:
                        if f.endswith('.exe'):
                            files.append(f)
                    for f in files:
                        cmd = ['chmod', '-cR', 'a+x', f'{dirpath}/{f}']
                        proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
                        jobs[op]['output'] += proc.stdout
        addJob(jobs, op, history, f, self.history_timeout)

    def permissoesExe(self):
        return self.permissoes(False)
