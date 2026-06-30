
import tempfile
import subprocess

from .check_output import check_result
from .format_input import format_cwd, format_env, format_input
from .utils import MTException, make_value_map

def run_command(f, command, cwd, value_map):
  line = command["cmd"].format(**value_map)
  cmd = line.split(' ')
  input = format_input(command, value_map)
  cwd1 = format_cwd(cwd, command, value_map)
  env1 = format_env(command, value_map)
  return f(command, cwd1, env1, cmd, input, value_map)

def run_commands(f, cwd, file, commands):
  value_map = make_value_map(file)
  try:
    results = [run_command(f, command, cwd, value_map) for command in commands]
    print("test success:", file)
    return results
  except MTException as e:
    msg = f"fail: {file}\n{e.message}"
    print(msg)
    return []
  except Exception as e:
    print(e)
    return []

def check_testcase(file, testcase):
  def f(command, cwd, env, cmd, input, value_map):
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input, env=env)
    check_result(command, result, value_map)
    return result

  with tempfile.TemporaryDirectory() as tmp_dir:
    return run_commands(f, tmp_dir, file, testcase.commands)

def exec_testcase(file, testcase):
  def f(command, cwd, env, cmd, input, value_map):
    print(' '.join(cmd))
    subprocess.run(cmd, cwd=cwd, input=input, env=env)
  run_commands(f, ".", file, testcase.commands)
