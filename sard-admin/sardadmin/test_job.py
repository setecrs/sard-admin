import unittest
import time
from subprocess import run, PIPE, STDOUT

from .job import addJob, listHistoryByName

class TestJob(unittest.TestCase):
    def test_echo(self):
        jobs = {}
        op = "A"
        history = []
        def func():
            cmd = ['echo', "job_test.py"]
            proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
            yield proc.stdout
        t1, t2 = addJob(jobs, op, history, func, timeout=1)
        t1.join()
        time.sleep(0.1) # wait for t2 to del jobs[op]
        self.assertEqual(len(jobs),0)
        self.assertEqual(len(history),1)
        self.assertEqual(history[0]['output'], "job_test.py\n")
        self.assertEqual(history[0]['running'], False)
        dur = history[0]['end'] - history[0]['start']
        self.assertGreater(dur, 0)
        t2.join()
        self.assertEqual(len(history),0)

    def test_echo2(self):
        jobs = {}
        op = "A"
        history = []
        def func():
            cmd = ['echo', "job_test.py"]
            proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
            jobs["A"]["output"] += proc.stdout
        t1, t2 = addJob(jobs, op, history, func, timeout=1)
        t1.join()
        time.sleep(0.1) # wait for t2 to del jobs[op]
        self.assertEqual(len(jobs),0)
        self.assertEqual(len(history),1)
        self.assertEqual(history[0]['output'], "job_test.py\n")
        self.assertEqual(history[0]['running'], False)
        dur = history[0]['end'] - history[0]['start']
        self.assertGreater(dur, 0)
        t2.join()
        self.assertEqual(len(history),0)

    def test_double(self):
        jobs = {}
        op = "A"
        history = []
        def func():
            cmd = ['sleep', "0.1"]
            proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
            yield proc.stdout
        tA1, tA2 = addJob(jobs, op, history, func, timeout=1)
        accepted = False
        try:
            tB1, tB2 = addJob(jobs, op, history, func, timeout=1)
            accepted = True
        except:
            pass
        if accepted:
            self.fail("should not accept two jobs with the same key")
        tA1.join()
        time.sleep(0.1)
        self.assertEqual(len(jobs),0)
        self.assertEqual(len(history),1)
        tA2.join()
        self.assertEqual(len(history),0)

    def test_listHistoryByName(self):
        jobs = {}
        op = "A"
        history = []
        def func():
            cmd = ['echo']
            proc = run(cmd, stdout=PIPE, stderr=STDOUT, check=True, encoding='utf-8')
            yield proc.stdout
        tA1, tA2 = addJob(jobs, op, history, func, timeout=1)
        tA1.join()
        got = listHistoryByName(history, 'A')
        self.assertEqual(len(got),1)
        self.assertEqual(got[0]['name'],'A')
        got = listHistoryByName(history, 'B')
        self.assertEqual(got,[])


