from os.path import exists

def check_file_exists(filename):
    if (not exists(filename)):
        raise RuntimeError("unable to locate file: '" + filename + "'")

def file_exists(filename):
    if (not exists(filename)):
        return False
    
    return True