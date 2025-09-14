#!/usr/bin/python3

import sys
import yaml

from .run_commands import run_build_commands
from .run_file import extract_file, remove_commands
from .traverse_directory import traverse, traverse_list 
from .utils import FileKind, cxxkind, pythonkind

class literal_unicode(str): pass

def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(literal_unicode, literal_unicode_representer)

def rewrite_file(filename, filekind: FileKind, commands):
  content1 = remove_commands(filename, filekind)
  yaml_content = yaml.dump(commands, Dumper=yaml.Dumper)
  content2 = f"{content1}\n\n{filekind.start_label}\n{yaml_content}\n{filekind.end_label}"
  with open(filename, "w") as file:
    file.write(content2)

def fill_command(command, result):
  stdout0 = command.get("stdout")
  stderr0 = command.get("stderr")
  status0 = command.get("status")
  # TODO: check match
  if stdout0 == None and stderr0 == None and status0 == None:
    command["stdout"] = literal_unicode(result.stdout.decode('utf-8'))
    command["stderr"] = literal_unicode(result.stderr.decode('utf-8'))
    command["status"] = result.returncode

def run_commands(filename, filekind: FileKind):
  commands = extract_file(filename, filekind)
  results = run_build_commands(filename, commands)
  for command, result in zip(commands, results):
    fill_command(command, result)
  rewrite_file(filename, filekind, commands)

def init_commands(filename, filekind: FileKind):
  with open(filename, "r+") as file:
    content = file.read()
    if -1 != content.find(filekind.start_label):
      print("already have commands:", filename)
    elif -1 != content.find(filekind.todo_label):
      print("already have todo commands:", filename)
    else:
      content = f"\n{filekind.start_label}\n- cmd: \n{filekind.end_label}\n"
      file.write(content)

def build_file(op, filekinds):
  op_commands = init_commands if op == "init" else run_commands
  def f(file):
    for filekind in filekinds:
      for suffix in filekind.suffixs:
        if file.endswith(suffix):
          op_commands(file, filekind)
  return f

def parseArgv(argv):
  index = 1
  op = 'init'
  while(index < len(argv)):
    if not argv[index].startswith('--') :
      break
    elif argv[index] == '--init':
      op = 'init'
      index = index + 1
    elif argv[index] == '--run':
      op = 'run'
      index = index + 1
    else:
      index = index + 1
  return (op, index)

if __name__ == "__main__":
  (op, index) = parseArgv(sys.argv)
  func = build_file(op, [cxxkind, pythonkind])
  traverse_list(func, sys.argv[index:])
