import os

__all__ = ['get_path']

_abpath = os.path.abspath(__file__)
example_dir = os.path.split(_abpath)[0]
base = example_dir
dirs = next(os.walk(base))[1]
file_2_dir = {}

for d in dirs:
    tmp = os.path.join(example_dir, d)
    files_in_tmp = os.listdir(tmp)
    for f in files_in_tmp:
        file_2_dir[f] = tmp


def get_path(example_name):
    """
    Get path of  example folders
    """
    if type(example_name) != str:
        try:
            example_name = str(example_name)
        except:
            raise KeyError('Cannot coerce requested example name to string')
    if example_name in dirs:
        return os.path.join(example_dir, example_name)
    elif example_name in file_2_dir:
        d = file_2_dir[example_name]
        return os.path.join(d, example_name)
    elif example_name == "":
        return os.path.join(base,  example_name)
    else:
        raise KeyError(example_name + ' not found in built-in examples.')


def available(verbose=False):
    """
    List available datasets
    """
    base = get_path('')
    print('base:',base)
    examples = [os.path.join(get_path(''), d) for d in os.listdir(base)]
    print('examples: ',examples)
    examples = [d for d in examples if os.path.isdir(d) and '__' not in d]
    if not verbose:
        return [os.path.split(d)[-1] for d in examples]
    examples = [os.path.join(dty, 'README.md') for dty in examples]
    descs = [_read_example(path) for path in examples]
    return [{desc['name']:desc['description'] for desc in descs}]


def _read_example(pth):
    try:
        with open(pth, 'r') as io:
            title = io.readline().strip('\n')
            io.readline()  # titling
            io.readline()  # pad
            short = io.readline().strip('\n')
            io.readline()  # subtitling
            io.readline()  # pad
            rest = io.readlines()
            rest = [l.strip('\n') for l in rest if l.strip('\n') != '']
            d = {'name': title, 'description': short, 'explanation': rest}
    except IOError:
        basename = os.path.split(pth)[-2]
        dirname = os.path.split(basename)[-1]
        d = {'name': dirname, 'description': None, 'explanation': None}
    return d


def explain(name):  # would be nice to use pandas for display here
    """
    Explain a dataset by name
    """
    path = get_path(name)
    fpath = os.path.join(path, 'README.md')
    print('path: ',path)
    print('fpath: ',fpath)
    return _read_example(fpath)
