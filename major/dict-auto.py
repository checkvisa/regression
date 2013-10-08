#!/usr/bin/env python
# Automatically complete the dictionary according to exisitng dictionary, 
# and Bayesian generative model that helps assesses similarity. 
# Usage: $0 old_dict input_list new_dict

import sys
import difflib

# read in the old dictionary
mdict={}
fin = open(sys.argv[1], 'r')
for line in fin:
  key_, value_ = line.strip().split(' ==> ')
  mdict[key_.lower()] = value_
  mdict[value_.lower()] = value_
fin.close()

# Read the input, and count the occurrences of each hypotheses.
# The hypothesis space includes each variation (length > 3) of each established major. 
# hycount[hypo] = prior
hycount = {}
fin = open(sys.argv[2], 'r')
for line in fin:
  line = line.strip().lower()
  # when a variation is encountered, its regular form also gets a count
  if line in mdict:
    if line in hycount:   hycount[line] += 1
    elif len(line)>3:     hycount[line] = 1

# Several useful definitions
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def abbr(word):
  return ''.join([x[0] for x in word.split()])

# http://norvig.com/spell-correct.html
def edits1(word):
  splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
  deletes    = [a + b[1:] for a, b in splits if b]
  transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
  replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
  inserts    = [a + c + b     for a, b in splits for c in alphabet]
  return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
  return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in hycount)
  
def known(words): return set(w for w in words if w in hycount)

# compute jaccard distance between the set of tokens in word1 and word2
def jaccard(word1, word2):
  set_a = set(word1.split())
  set_b = set(word2.split())
  return float(len(set_a.intersection(set_b))) / len(set_a.union(set_b))

# finding the length of the longest overlap between two strings
# http://stackoverflow.com/questions/14128763/how-to-find-the-overlap-between-2-sequences-and-return-it
def longest_match(word1, word2):
  d = difflib.SequenceMatcher(None, word1, word2)
  a,b,size = max(d.get_matching_blocks(),key=lambda x:x[2])
  return size

# find all possible hypotheses
# return: [hypo] = likelihood
def find_hypos(word):
  like = dict(hycount)
  for h in like: 
    # Stage 1: baseline
    like[h] = 1e-6
    # Stage 2: token match
    like[h] = max(jaccard(h, word), like[h])
    # Stage 3: acronym match (suppose query is full)
    abb1 = abbr(word)
    abb2 = abbr(h)
    if len(abb1)>1 and len(abb2)>1:
      abb_inter = longest_match(abb1, abb2)
      abb_total = len(abb1) + len(abb2)
      like[h] = max(float(abb_inter)*1.0/abb_total, like[h])
    # Stage 4: acronym match (suppose query is acro)
    if len(abb2)>1:
      abb_inter = longest_match(word, abb2)
      abb_total = len(word) + len(abb2)
      like[h] = max(float(abb_inter)*2.0/abb_total, like[h])
    # Stage 5: sequence overlapping (sharing prefix/affix)
    seq_inter = longest_match(word, h)
    seq_total = len(word) + len(h)
    like[h] = max(float(seq_inter)*0.5/seq_total, like[h])
  # Stage 6: one-edits
  for h in known(edits1(word)):
    like[h] = max(0.9, like[h])
  # Stage 7: two-edits
  for h in known_edits2(word):
    like[h] = max(0.8, like[h])
  return like

# Read again the input, and force-map each unmatched input 
# to a mdict entry using a Bayesian generative model. Save
# the result as a new version of mdict.
fin.seek(0)
linecount = 0
for line in fin:
  linecount += 1
  line = line.strip().lower()
  if line in mdict: 
    continue
  else:
    likelihood = find_hypos(line)
    max_post = -1
    hmax = 'na'
    for h in likelihood:
      # NOTE!!!
      # Here I commented out the prior probability. Because some majors that are too dominating are undesirable.
      posterior = likelihood[h] #* hycount[h]
      if posterior > max_post:
        max_post = posterior
        hmax = h
    mdict[line] = mdict[hmax]
    sys.stderr.write(str(linecount)+': '+line+' ==> '+hmax+' | like='+str(likelihood[hmax])+'\n')
fin.close()

fout = open(sys.argv[3], 'w')
for key in mdict:
  if len(key.strip())>=1:
    fout.write(key + " ==> " + mdict[key] + "\n")
fout.close()
