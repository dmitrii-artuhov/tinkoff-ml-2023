from os.path import exists

def check_file_exists(filename):
    if (not exists(filename)):
        raise RuntimeError("unable to locate file: '" + filename + "'")

def file_exists(filename):
    if (not exists(filename)):
        return False
    
    return True


def print_matrix(mat):
    n = len(mat)
    m = len(mat[0])

    for i in range(0, n):
        s = ""
        for j in range(0, m):
            s += f"{mat[i][j]} "
        print(s)

