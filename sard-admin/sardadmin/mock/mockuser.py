from .mockgroup import Group

class User:
    _all = [
        'root',
        'nobody',
    ]
    _passwords = {}
    _running = []
    
    @staticmethod
    def listAll():
        return User._all[:]

    def __init__(self, name):
        self.name = name

    def uid(self):
        return User._all.index(self.name)
    
    def exists(self):
        return self.name in User._all

    def groups(self):
        result = []
        for g,members in Group._members.items():
            if self.name in members:
                result.append(g)
        return result

    def create(self, password=None):
        if self.exists():
            raise Exception('user already exists')
        User._all.append(self.name)
        self.permissions()
        Group(self.name).create()
        self.enterGroup(self.name)
        self.enterGroup('Domain Users')
        return self.resetPassword(password)

    def delete(self):
        if not self.exists():
            raise Exception('user does not exist')
        User._all.pop(self.uid())
        del User._passwords[self.name]
        Group(self.name).delete()

    def enterGroup(self, group):
        if not Group(group).exists:
            raise Exception('group does not exist')
        Group._members[group].append(self.name)

    def resetPassword(self, password=None):
        if password is None:
            password = self.name + '_pass'
        User._passwords[self.name] = password
        return password

    def permissions(self):
        if self.name in User._running:
            raise Exception('already running')
        User._running.append(self.name)

    def populateHome(self):
        return
