#!/usr/bin/python3

import sys
from run_file import run_file
from traverse_directory import traverse 
from utils import cxxkind, pythonkind

def parseArgv(argv):
  index = 1
  mode = 'check'
  while(index < len(argv)):
    if not argv[index].startswith('--') :
      break
    elif argv[index] == '--exec':
      mode = 'exec'
      index = index + 1
    elif argv[index] == '--check':
      mode = 'check'
      index = index + 1
    else:
      index = index + 1
  return (mode, index)

if __name__ == "__main__":
  (mode, index) = parseArgv(sys.argv)
  func = run_file(mode, [cxxkind, pythonkind])
  traverse(func, sys.argv[index:])
