
import re

def push_value(value_map, id, value):
  v = value_map.get(id)
  if v == None:
    value_map[id] = value
  else:
    raise Exception("id already exists: ", id)

def equal_pattern(target: str, argv: str, value_map):
  id = argv
  value = value_map.get(argv)
  if value == None:
    raise Exception("id does not exist: ", id)
  elif not target.startswith(value):
    raise Exception("value unmatch, id: ", id)
  else:
    return target[len(value):]

def regex_pattern0(target: str, value_map, id: str, regex: str):
  r = re.match(regex, target)
  if r:
    if id:
      push_value(value_map, id, r.group())
    return target[r.end():]
  else:
    raise Exception("not match")

def make_regex_pattern(regex: str):
  def match_pat(target: str, argv: str, value_map):
    return regex_pattern0(target, value_map, argv, regex)
  return match_pat

def regex_pattern(target: str, argv: str, value_map):
  (id, regex) = argv.split(",", 1)
  id1 = id.strip()
  regex1 = regex.strip()
  return regex_pattern0(target, value_map, id1, regex1)

patterns = [
  ("eq", equal_pattern),
  ("dec", make_regex_pattern(r'-?[0-9]*')),
  ("hex", make_regex_pattern(r'0x[0-9a-fA-F]*')), 
  ("regex", regex_pattern),
]

def add_pattern(pat, match_pat):
  patterns.append((pat, match_pat))

def find_pattern(exp: str):
  for (pat, match_pat) in patterns:
    if exp.startswith(pat):
      return (pat, match_pat)
  return None

def parse_argv(argv):
  if len(argv) == 0:
    return ""
  elif argv[0] != ":":
    raise "need ':': " + argv
  else:
    return argv[1:].strip()

def match_pattern(expect: str, target: str, value_map, pattern):
  (pat, match_pat) = pattern
  pat_len = len(pat)
  last0 = expect[pat_len: ]
  [argv, expect1] = last0.split("}", 1)
  argv1 = parse_argv(argv)
  target1 = match_pat(target, argv1, value_map)
  match_string(expect1, target1, value_map)

def match_expect(expect: str, target: str, value_map):
  pattern = find_pattern(expect)
  if pattern == None:
    match_string(expect, target[1:], value_map)
  else:
    match_pattern(expect, target, value_map, pattern)

def match_lit(expect: str, target: str, value_map):
  result = expect.split("{", 1)
  exp = result[0]
  assert(target.startswith(exp))
  target1 = target[len(exp):]
  if len(result) == 1:
    assert(len(target1) == 0)
  else:
    match_expect(result[1], target1, value_map)

def match_string(expect: str, target: str, value_map):
  expect_remain = len(expect) > 0 
  target_remain = len(target) > 0
  if expect_remain:
    if target_remain:
      match_lit(expect, target, value_map)
    else:
      raise Exception("target exhaustion")
  elif target_remain:
      raise Exception("expect exhaustion")
