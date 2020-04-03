from collections import defaultdict

from ..job import addJob, AlreadyRunningException

class Group:
    jobs = {}
    history = []
    _all = [
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
    _members = defaultdict(lambda: [])
    _running=[]

    @staticmethod
    def listAll():
        return Group._all[:]

    def __init__(self, name, history_timeout=0):
        self.name = name
        self.history_timeout = history_timeout

    def gid(self):
        return Group._all.index(self.name)

    def exists(self):
        return self.name in Group._all

    def users(self):
        return Group._members[self.name]

    def create(self):
        if self.exists():
            raise Exception('group already exists')
        self.permissions()
        Group._all.append(self.name)

    def delete(self):
        Group._all.pop(self.gid())
        Group._running.pop(Group._running.index(self.name))
        
    def permissions(self):
        if self.name in Group._running:
            raise Exception('already running')
        Group._running.append(self.name)
        
    def permissions(self):
        if self.name in Group._running:
            raise AlreadyRunningException
        Group._running.append(self.name)
        def f():
            pass
        addJob(Group.jobs, self.name, Group.history, f, self.history_timeout)
