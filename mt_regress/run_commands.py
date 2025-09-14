
import tempfile
import subprocess

from .check_output import check_output, check_status
from .format_input import format_cwd, format_input
from .utils import MTException, make_value_map

def run_command(f, command, cwd, value_map):
  line = command["cmd"].format(**value_map)
  cmd = line.split(' ')
  input = format_input(command, value_map)
  cwd1 = format_cwd(cwd, command, value_map)
  return f(command, cwd1, cmd, input, value_map)

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

def run_check_commands(file, commands):
  def f(command, cwd, cmd, input, value_map):
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input)
    check_output(command, "stdout", result.stdout.decode('utf-8'), value_map)
    check_output(command, "stderr", result.stderr.decode('utf-8'), value_map)
    check_status(command, result.returncode, value_map)

  with tempfile.TemporaryDirectory() as tmp_dir:
    run_commands(f, tmp_dir, file, commands)

def run_exec_commands(file, commands):
  def f(command, cwd, cmd, input, value_map):
    print(' '.join(cmd))
    subprocess.run(cmd, cwd=cwd, input=input)
  run_commands(f, ".", file, commands)

def run_build_commands(file, commands):
  def f(command, cwd, cmd, input, value_map):
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input)
    return result

  with tempfile.TemporaryDirectory() as tmp_dir:
    return run_commands(f, tmp_dir, file, commands)
