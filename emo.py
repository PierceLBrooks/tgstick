
# Author: Pierce Brooks

import os
import sys

descriptor = open(os.path.join(os.getcwd(), "emoji.txt"), "r", encoding="raw_unicode_escape")
lines = descriptor.readlines()
descriptor.close()
content = []
buffer = "'"
codes = []
for line in lines:
  line = line.strip()
  if (len(line) == 0):
    continue
  if (line.startswith("#")):
    continue
  line = line.split(";")
  line = line[0].strip()
  if (" " in line):
    continue
  if (len(line) == 5):
    buffer += "\\U000"+line
  elif (len(line) == 4):
    buffer += "\\u"+line
  else:
    continue
  print(line)
  codes.append(line)
  if (len(buffer) > 200):
    buffer += "' \\"
    content.append(buffer)
    buffer = "'"
print(str(len(codes)))
descriptor = open(os.path.join(os.getcwd(), sys.argv[0]+".txt"), "w")
for line in content:
  descriptor.write(line+"\n")
descriptor.close()
