
import concurrent.futures
import os

def check_directory(executor, ps, f, rootdir):
  for dir in os.walk(rootdir):
    for filename in dir[2]:
      file = os.path.join(dir[0], filename)
      p = executor.submit(f, file)
      ps.append(p)

def traverse(f, args):
  with concurrent.futures.ThreadPoolExecutor() as executor:
    ps = []
    for arg in args:
      if os.path.isdir(arg):
        check_directory(executor, ps, f, arg)
      elif os.path.isfile(arg):
        p = executor.submit(f, arg)
        ps.append(p)
    
    return [p.result() for p in ps]

def traverse_list(f, args):
  with concurrent.futures.ThreadPoolExecutor() as executor:
    ps = executor.map(f, args)
    return [r for r in ps]
