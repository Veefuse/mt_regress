#!/usr/bin/python3

import sys

from .build_testcase import init_testcase, build_testcase
from .run_testcase import check_testcase, exec_testcase
from .extract_file import extract_file
from .traverse_directory import traverse 
from .utils import init_yaml, cxxkind, pythonkind

def parseArgv(argv):
  index = 1
  mode = "check"
  filekinds = [cxxkind, pythonkind]
  while(index < len(argv)):
    arg = argv[index]
    if not arg.startswith('--') :
      break

    elif arg == '--init':
      mode = "init"
    elif arg == '--build':
      mode = "build"
    elif arg == '--exec':
      mode = "exec"
    elif arg == '--check':
      mode = "check"
      filekinds = [cxxkind, pythonkind]

    index = index + 1
  return (mode, filekinds, index)

def run_file1(func, filename, filekinds):
  testcases = extract_file(filename, filekinds)
  for testcase in testcases:
    func(filename, testcase)
            
def run_file(mode, filekinds):
  def f(filename):
    if mode == "init":
      init_testcase(filename, filekinds)
    elif mode == "build":
      run_file1(build_testcase, filename, filekinds)
    elif mode == "exec":
      run_file1(exec_testcase, filename, filekinds)
    else:
      run_file1(check_testcase, filename, filekinds)

  return f

def main():
  init_yaml()
  (mode, filekinds, index) = parseArgv(sys.argv)
  func = run_file(mode, filekinds)
  traverse(func, sys.argv[index:])

if __name__ == "__main__":
  main()