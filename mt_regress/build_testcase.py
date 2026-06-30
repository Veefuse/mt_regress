
import yaml

from .utils import FileKind, literal_unicode, TestCase
from .run_testcase import check_testcase
from .extract_file import extract_file, match_filekinds

def rewrite1(content, testcase):
  commands = testcase.commands
  filekind = testcase.filekind
  start_label = filekind.start_label
  end_label = filekind.end_label

  [before_start, last0] = content.split(start_label, 1)
  [old_commands, after_end] = last0.split(end_label, 1)
  
  yaml_content = yaml.dump(commands, Dumper=yaml.Dumper)
  content1 = f"{before_start}{start_label}\n{yaml_content}\n{end_label}"
  return content1, after_end

def rewrite_content(content, testcases):
  if len(testcases) == 0:
    return content
  else:
    content1, after_end  = rewrite1(content, testcases[0])
    content2 = rewrite_content(after_end, testcases[1:])
    return content1 + content2

def rewrite_file(filename, testcases):
  content1 = ""
  with open(filename, "r") as file:
    content = file.read()
    content1 = rewrite_content(content, testcases)

  with open(filename, "w") as file:
    file.write(content1)

def fill_command(command, result):
  stdout0 = command.get("stdout")
  stderr0 = command.get("stderr")
  status0 = command.get("status")
  if stdout0 == None and stderr0 == None and status0 == None:
    command["stdout"] = literal_unicode(result.stdout.decode('utf-8'))
    command["stderr"] = literal_unicode(result.stderr.decode('utf-8'))
    command["status"] = result.returncode

def build_testcases(filename, filekinds):
  testcases = extract_file(filename, filekinds)
  for testcase in testcases:
    commands = testcase.commands
    results = check_testcase(filename, testcase)
    for command, result in zip(commands, results):
      fill_command(command, result)
  rewrite_file(filename, testcases)

def init_testcases(filename, filekinds):
  filekinds1 = match_filekinds(filename, filekinds)
  with open(filename, "a") as file:
    for filekind in filekinds1:
      seg = f"\n{filekind.start_label}\n- cmd: \n{filekind.end_label}\n"
      file.write(seg)
