
import os
import re
import yaml

class literal_unicode(str): pass

def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')

def init_yaml():
  yaml.add_representer(literal_unicode, literal_unicode_representer)

class MTException(Exception):
  def __init__(self, message, *args, **kwargs):
    super().__init__(message, *args, **kwargs)
    self.message = message

def make_value_map(filename):
  curfile = os.path.abspath(filename)
  curdir = os.path.dirname(curfile)
  return { "curfile": curfile, "curdir": curdir }

class FileKind:
  def __init__(self, regex, start_label, end_label):
    self.regex = regex
    self.start_label = start_label
    self.end_label   = end_label


cxx_regex = re.compile(r".*\.(c|cpp|cxx|cc)$")
cxxkind = FileKind(cxx_regex, "#ifdef MTTest", "#endif")
cxxTodoKind = FileKind(cxx_regex, "#ifdef TodoMTTest", "#endif")

py_regex = re.compile(r".*\.py$")
pythonkind = FileKind(py_regex, '"""MTTest', '"""')
pythonTodokind = FileKind(py_regex, '"""TodoMTTest', '"""')

class TestCase:
  def __init__(self, filekind, commands):
    self.filekind = filekind
    self.commands = commands