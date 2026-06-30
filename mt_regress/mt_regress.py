#!/usr/bin/python3

import sys

from .options import parseArgv
from .build_testcase import init_testcases, build_testcases
from .run_testcase import check_testcase, exec_testcase
from .extract_file import extract_file
from .traverse_directory import traverse 
from .utils import init_yaml, cxxkind, pythonkind, cxxTodoKind, pythonTodokind

def run_file1(func, filename, filekinds):
  testcases = extract_file(filename, filekinds)
  for testcase in testcases:
    func(filename, testcase)
            
def run_file(mode):
  filekinds0 = [cxxkind, pythonkind]
  filekinds1 = [cxxkind, pythonkind, cxxTodoKind, pythonTodokind]
  def f(filename):
    if mode == "init":
      init_testcases(filename, filekinds0)
    elif mode == "build":
      build_testcases(filename, filekinds1)
    elif mode == "exec":
      run_file1(exec_testcase, filename, filekinds1)
    else:
      run_file1(check_testcase, filename, filekinds0)

  return f

def main():
  init_yaml()
  (mode, files) = parseArgv(sys.argv)
  func = run_file(mode)
  traverse(func, files)

if __name__ == "__main__":
  main()