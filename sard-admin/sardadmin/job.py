import time
import types
from threading import Thread

class AlreadyRunningException(Exception):
    "Job already running"
    pass

def listHistoryByName(history, name):
    byName = [h for h in history if h['name'] == name]
    serializable = [dict((k, h[k]) for k in h if k != 'thread') for h in byName]
    return serializable

def addJob(jobs, op, history, func, timeout):
    if op in jobs:
        raise AlreadyRunningException(f'op already in job list: {op}')
    def th():
        jobs[op] = {
            "name": op,
            "running": True,
            "start": time.time(),
            "end": None,
            "output": "",
        }
        result = func()
        if isinstance(result, types.GeneratorType):
            for x in result:
                jobs[op]['output'] +=x + '\n'
    t1 = Thread(target=th)
    t1.start()
    jobs[op]['thread']=t1
    history.append(jobs[op])
    def monitor():
        t = jobs[op]['thread']
        t.join()
        jobs[op]['running'] = False
        jobs[op]['end'] = time.time()
        obj = jobs[op]
        del jobs[op]
        time.sleep(timeout)
        history.pop(history.index(obj))
    t2 = Thread(target=monitor)
    t2.start()
    return t1, t2
