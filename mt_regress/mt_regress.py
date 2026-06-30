#!/usr/bin/python3

import sys
from .run_file import run_file
from .run_commands import run_check_commands, run_exec_commands
from .traverse_directory import traverse 
from .utils import cxxkind, pythonkind

def parseArgv(argv):
  index = 1
  mode = run_check_commands
  filekinds = [cxxkind, pythonkind]
  while(index < len(argv)):
    if not argv[index].startswith('--') :
      break
    elif argv[index] == '--run':
      mode = run_exec_commands
      index = index + 1
    elif argv[index] == '--check':
      mode = run_check_commands
      filekinds = [cxxkind, pythonkind]
      index = index + 1
    else:
      index = index + 1
  return (mode, filekinds, index)

def main():
  (mode, filekinds, index) = parseArgv(sys.argv)
  func = run_file(mode, filekinds)
  traverse(func, sys.argv[index:])

if __name__ == "__main__":
  main()