import os
import subprocess

_filters = "-build/c++11"
_include_ext = "hpp, cuh, cu, c, hxx, c++, h, cc, h++, hh, cpp, cxx"
_exclude_ext = "pb.h, pb.cc"
_linelength = 120

def check_file(filepath):
    subprocess.run(f'cpplint --quiet --filter={_filters} --linelength={_linelength} {filepath}', shell=True)

def run_cpplint(paths, linelength):
    _linelength = linelength
    include_exts = tuple([x.strip() for x in _include_ext.split(',')])
    exclude_exts = tuple([x.strip() for x in _exclude_ext.split(',')])
    assert isinstance(paths, list)
    for path in paths:
        if os.path.isfile(path):
            check_file(path)
            continue
        if not os.path.exists(path):
            print("[error] path not exists:", path)
        for root, folders, files in os.walk(path):
            for file in files:
                if file.endswith(include_exts) and not file.endswith(exclude_exts):
                    filepath = os.path.join(root, file)
                    check_file(filepath)

