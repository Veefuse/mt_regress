
from .utils import MTException

def format_stdin(command, value_map):
  stdin0 = command.get("stdin")
  if stdin0 == None:
    return None
  elif isinstance(stdin0, str):
    filename = stdin0.format(**value_map)
    with open(filename, "r") as file1:
      content = file1.read()
      return content.format(**value_map).encode('utf-8')
  else:
    raise MTException("unknown stdin type:" + stdin0)

def format_input(command, value_map):
  input0 = command.get("input")
  if input0 == None:
    return format_stdin(command, value_map)
  elif isinstance(input0, str):
    return input0.format(**value_map).encode('utf-8')
  else:
    raise MTException("unknown input type:" + input0)

def format_cwd(cwd0, command, value_map):
  cwd1 = command.get("cwd")
  if cwd1 == None:
    return cwd0
  elif isinstance(cwd1, str):
    return cwd1.format(**value_map)
  else:
    raise MTException("unknown cwd type:" + cwd1)