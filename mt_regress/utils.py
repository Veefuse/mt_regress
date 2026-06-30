
import os
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
  def __init__(self, suffixs, start_label, end_label):
    self.suffixs     = suffixs
    self.start_label = start_label
    self.end_label   = end_label

cxxkind = FileKind([".c", ".cpp", ".cxx", ".cc"], "#ifdef MTTest", "#endif")
pythonkind = FileKind([".py"] , '"""MTTest', '"""')

cxxTodoKind = FileKind([".c", ".cpp", ".cxx", ".cc"], "#ifdef TodoMTTest", "#endif")
pythonTodokind = FileKind([".py"] , '"""TodoMTTest', '"""')

class TestCase:
  def __init__(self, filekind, commands):
    self.filekind = filekind
    self.commands = commands