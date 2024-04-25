import codecs
import os


def get_discription(file_path='README.rst', folder=os.getcwd()):
    with codecs.open("{}/{}".format(folder, file_path), 'r', encoding='utf-8') as readme:
        return readme.read()


def load_requirements(file_name, folder=os.getcwd()):
    with codecs.open(os.path.join(folder, file_name), 'r', encoding='utf-8')as req_file:
        return req_file.read().strip().split('\n')


def listfiles(folder):
    if not isinstance(folder, (list, tuple)):
        folder = [folder]
    folder = filter(lambda p: os.path.isdir(p), folder)
    for one_folder in folder:
        for root, folders, files in os.walk(one_folder):
            for filename in folders + files:
                yield os.path.join(root, filename)
