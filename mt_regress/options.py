
help_message = """
usage: mt_regress [mode] <file or directory>*

mode:
  --init            init testcase
  --build           build testcase
  --exec            execute testcase
  --check           check testcase (default)

options:
  --help            show help message
  --version         show version message
"""

def parseArgv(argv):
  index = 1
  mode = "check"
  while(index < len(argv)):
    arg = argv[index]
    if not arg.startswith('--') :
      break

    elif arg == '--init':
      mode = "init"
    elif arg == '--build':
      mode = "build"
    elif arg == '--exec':
      mode = "exec"
    elif arg == '--check':
      mode = "check"

    elif arg == '--version':
      print("mt_regress 1.0.2")
      exit(0)
    
    elif arg == '--help':
      print(help_message)
      exit(0)

    else:
      print("unknown argument:", arg)
      exit(0)

    index = index + 1
  return (mode, argv[index:])