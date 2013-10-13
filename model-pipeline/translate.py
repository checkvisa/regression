#!/usr/bin/env python
# Usage: ./translate.py dict dat dat_translated

import sys

# read in the dictionary
mdict={}
fin = open(sys.argv[1], 'r')
for line in fin:
  key_, value_ = line.strip().split(' ==> ')
  mdict[key_.lower()] = value_
  mdict[value_.lower()] = value_
fin.close()

# read through the input dat.tsv and translate the major (5th column)
fin = open(sys.argv[2], 'r')
fout = open(sys.argv[3], 'w')
for line in fin:
  fs = line.strip().split('\t')
  if len(fs) < 5:
    continue
  major = fs[4].lower()
  if not major in mdict:
    sys.stderr.write("error: %s not in dictionary. Skipped.\n"%major)
    continue
  major_translated = mdict[major]
  fs[4] = major_translated
  fout.write('\t'.join(fs)+'\n')
fin.close()
fout.close()

