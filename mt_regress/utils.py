
import os

class MTException(Exception):
  def __init__(self, message, *args, **kwargs):
    super().__init__(message, *args, **kwargs)
    self.message = message

def make_value_map(filename):
  curfile = os.path.abspath(filename)
  curdir = os.path.dirname(curfile)
  return { "curfile": curfile, "curdir": curdir }

class FileKind:
  def __init__(self, suffixs, start_label, end_label, todo_label):
    self.suffixs     = suffixs
    self.start_label = start_label
    self.end_label   = end_label
    self.todo_label  = todo_label

cxxkind = FileKind([".c", ".cpp", ".cxx", ".cc"], "#ifdef MTTest", "#endif", "#ifdef TodoMTTest")
pythonkind = FileKind([".py"] , '"""MTTest', '"""', '"""TodoMTTest')
