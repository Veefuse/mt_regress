
import yaml
from .utils import TestCase

def remove_commands(filename, filekind):
  with open(filename, "r") as file:
    content = file.read()
    ss = content.split(filekind.start_label)
    prices = [ss[0]]
    for s in ss[1:]:
      r = s.split(filekind.end_label)
      if len(r) == 2:
        prices.append(r[1])

    return ''.join(prices).rstrip()

def extract_testcases(content, filekind):
  ss = content.split(filekind.start_label)[1:]
  yaml_contents = [s.split(filekind.end_label)[0] for s in ss]

  testcases = []
  for y in yaml_contents:
    commands = yaml.load(stream = y, Loader = yaml.FullLoader)
    testcase = TestCase(filekind, commands)
    testcases.append(testcase)
  return testcases

def extract_all_testcases(filename, filekinds):
  with open(filename, "r") as file:
    content = file.read()
    testcases = []
    for filekind in filekinds:
      cases = extract_testcases(content, filekind) 
      testcases += cases
    return testcases

def match_filekinds(filename, filekinds):
  s = []
  for filekind in filekinds:
    if filekind.regex.search(filename):
      s.append(filekind)
  return s

def extract_file(filename, filekinds):
  filekinds1 = match_filekinds(filename, filekinds)
  if len(filekinds1) == 0:
    return []
  else:
    testcases = extract_all_testcases(filename, filekinds1)
    if len(testcases) == 0:
      print("leak test command:", filename)
    return testcases
 