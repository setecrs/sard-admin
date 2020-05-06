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
