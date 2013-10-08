#!/usr/bin/env python
# Usage: $0 dictionary value_list

import sys
from sys import argv
import codecs

mdict={}
values={}
fin = codecs.open(argv[1], 'r')
for line in fin:
  fs = line.strip().split(' ==> ')
  if len(fs)<2: continue
  mdict[fs[0]] = fs[1]
  values[fs[1]] = 1
fin.close()

fin = codecs.open(argv[2], 'r')
linecount = 0
for line in fin:
  linecount += 1
  line = line.strip()
  if line in mdict: continue
  else:
    print("\n%d: "%linecount + line)
    values_ = values.keys()
    values_.sort()
    for i in range(len(values_)):
      print("  [%d] %s"%(i, values_[i]))
    user_answer = raw_input("Select or Create:")
    if user_answer.isdigit():
      mdict[line] = values_[int(user_answer)]
    elif user_answer != "":
      values[user_answer] = 1
      mdict[line] = user_answer
    else:
      sys.stderr.write("Processed %d lines\n"%(linecount-1))
      break
fin.close()

fout = codecs.open(argv[1], 'w')
for key in mdict:
  fout.write(key + " ==> " + mdict[key] + "\n")
fout.close()
