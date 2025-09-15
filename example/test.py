
import os

print(os.environ)

"""MTTest
- cmd: python3 {curfile}
  status: 0
  stderr: ""
  env: 
    "": ""
    aaa: aaaa
    bbb: bb {curfile}
  stdout: |
    30

"""