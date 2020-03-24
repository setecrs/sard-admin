import subprocess

def command(s):
    print(s)
    yield s + '\n'
    p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.communicate():
        if line:
            print(line)
            yield line + '\n'
    if p.returncode != 0:
        raise Exception('Return code not zero.')
