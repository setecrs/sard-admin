import os


def count_sard_folders(imagepath):
    counter = 0
    dirname = os.path.dirname(imagepath)
    for item in os.listdir(dirname):
        if os.path.isdir(os.path.join(dirname, item)):
            if item.startswith('SARD'):
                counter += 1
    return counter


class FailedToRename(Exception):
    pass


def rename_sard_folder(imagepath):
    dirname = os.path.dirname(imagepath)
    sardfolder = os.path.join(dirname, 'SARD')
    if not os.path.exists(sardfolder):
        return False
    newsardfolder = os.path.join(dirname, 'SARD.old')
    if os.path.exists(newsardfolder):
        def nextFolder(newsardfolder):
            for x in range(2, 20):
                if not os.path.exists(newsardfolder+str(x)):
                    return newsardfolder+str(x)
            raise FailedToRename(newsardfolder)
        newsardfolder = nextFolder(newsardfolder)
    os.rename(sardfolder, newsardfolder)
    return True

def listSubfolders(group, subpath=''):
    xpath = f'/operacoes/{group}/{subpath}'
    xpath = xpath.rstrip('/')
    assert xpath == os.path.abspath(xpath)
    content = os.listdir(xpath)
    result = set()
    for x in content:
        fpath = os.path.join(xpath, x)
        if os.path.islink(fpath):
            continue
        if os.path.isfile(fpath):
            continue
        if os.path.isdir(fpath):
            result.add(x)
    return sorted(result)

def default_rw_mode(xpath, isDir=None):
    if isDir is None:
        isDir = os.path.isdir(xpath)
    return default_ro_mode(xpath, isDir) + 0o020

def default_ro_mode(xpath, isDir=None):
    if isDir is None:
        isDir = os.path.isdir(xpath)
    xpath = xpath.rstrip('/')
    assert xpath == os.path.abspath(xpath)
    if isDir:
        return 0o050
    if 'indexador/tools' in xpath:
        return 0o050
    if 'indexador/jre/bin' in xpath:
        return 0o050
    if 'indexador/lib' in xpath:
        return 0o050
    if xpath.endswith('.exe'):
        return 0o050
    return 0o040

def check_rw(xpath):
    xpath = xpath.rstrip('/')
    assert xpath == os.path.abspath(xpath)
    stat :os.stat_result = os.stat(xpath)
    return (stat.st_mode & 0o777) == default_rw_mode(xpath, os.path.isdir(xpath))

def check_ro(xpath):
    xpath = xpath.rstrip('/')
    assert xpath == os.path.abspath(xpath)
    stat :os.stat_result = os.stat(xpath)
    return (stat.st_mode & 0o777) == default_ro_mode(xpath, os.path.isdir(xpath))

def set_rw(xpath):
    if not check_rw(xpath):
        os.chmod(xpath, default_rw_mode(xpath))

def set_ro(xpath):
    if not check_ro(xpath):
        os.chmod(xpath, default_ro_mode(xpath))

def check_owner(xpath, gid):
    xpath = xpath.rstrip('/')
    assert xpath == os.path.abspath(xpath)
    stat :os.stat_result = os.stat(xpath)
    return stat.st_gid == gid and stat.st_uid == 0

def set_owner(xpath, gid):
    if not check_owner(xpath):
        os.chown(xpath, 0, gid)