
from .match_string import match_string
from .utils import MTException

def report_unmatch(prop, expect, actual):
  message = f"""
expect {prop}:
{expect}
actual {prop}:
{actual}
"""
  raise MTException(message)

def check_output(command, prop, actual, value_map):
  expect = command.get(prop)

  if expect == None:
    return
  elif not isinstance(expect, str):
    raise MTException(f"unknown {prop} type: {expect}")

  try:
    match_string(expect, actual, value_map)
  except:
    report_unmatch(prop, expect, actual)
 
def check_status(command, actual, value_map):
  prop = "status"
  expect = command.get(prop)
  if expect == None:
    return
  elif isinstance(expect, int):
    if expect != actual:
      report_unmatch(prop, expect, actual)
  elif isinstance(expect, str):
    check_output(command, "status", str(actual), value_map)
  else:
    raise MTException("unknown status type:" + expect)

def check_result(command, result, value_map):
  check_output(command, "stdout", result.stdout.decode('utf-8'), value_map)
  check_output(command, "stderr", result.stderr.decode('utf-8'), value_map)
  check_status(command, result.returncode, value_map)
