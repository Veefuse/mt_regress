#!/usr/bin/python3

import yaml

from .utils import FileKind, literal_unicode
from .extract_file import remove_commands

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
  if stdout0 == None and stderr0 == None and status0 == None:
    command["stdout"] = literal_unicode(result.stdout.decode('utf-8'))
    command["stderr"] = literal_unicode(result.stderr.decode('utf-8'))
    command["status"] = result.returncode

def build_testcase(filename, filekind: FileKind):
  return
  # commands = extract_file(filename, filekind)
  # results = run_check_commands(filename, commands)
  # for command, result in zip(commands, results):
  #   fill_command(command, result)
  # rewrite_file(filename, filekind, commands)

def init_testcase(filename, filekind: FileKind):
  with open(filename, "r+") as file:
    content = file.read()
    content = f"\n{filekind.start_label}\n- cmd: \n{filekind.end_label}\n"
    file.write(content)
