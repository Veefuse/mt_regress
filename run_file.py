
import yaml
from run_commands import run_check_commands, run_exec_commands

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

def extract_commands(filename, filekind):
  with open(filename, "r") as file:
    content = file.read()
    if content.find(filekind.todo_label) != -1: 
      print("todo:", filename)
      return []

    ss = content.split(filekind.start_label)[1:]
    yaml_contents = [s.split(filekind.end_label)[0] for s in ss]

    if len(yaml_contents) == 0:
      print("leak test command:", filename)
      return []

    commands = []
    for y in yaml_contents:
      cmds = yaml.load(stream = y, Loader = yaml.FullLoader)
      commands += cmds
    return commands

def extract_file(file, filekind):
  for suffix in filekind.suffixs:
    if file.endswith(suffix):
      return extract_commands(file, filekind)
  return []

def run_file(mode, filekinds):
  run_commands = run_exec_commands if mode == "exec" else run_check_commands
  def f(file):
    for filekind in filekinds:
      commands = extract_file(file, filekind)
      if len(commands) > 0:
        run_commands(file, commands)
  return f
