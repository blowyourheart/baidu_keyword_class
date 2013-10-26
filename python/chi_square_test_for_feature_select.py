#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-08-28 14:54:34

import sys
import os
import logging



def ChiSquareTest(Y, X, minDF = 3, topK = 2000):
  """
    input:
     Y: [label1 label2 ...]
     X: [label1 word0 word1 ...]
     topK: return the topK chi value per category
    output:
      {category:set(word), ....}
    """
  N = len(Y)
  category_cnt = {}
  word_label_cnt = {}

  for i in xrange(N):
    logging.debug("processing a record")
    label = Y[i]
    if label in category_cnt:
      category_cnt[label] += 1
    else:
      category_cnt[label] = 1

    for w in X[i]:
      if w in word_label_cnt:
        if label in word_label_cnt[w]:
          word_label_cnt[w][label] += 1
        else:
          word_label_cnt[w][label] = 1
      else:
        word_label_cnt[w] = {}
        word_label_cnt[w][label] = 1
  logging.info("store X done")

  #Compute X-chi value for (category, w) pair
  res_per_category = {}
  for (label, n_label) in category_cnt.items():
    res = []
    for (w, dis) in word_label_cnt.items():
      logging.debug("processing %s %s"%(label, w))
      total_occur = sum([v for (k, v) in dis.items()])
      if total_occur < minDF:
        logging.debug("%s DF = %d"%(w, total_occur))
        continue
      if label in dis:
        A = dis[label]
        B = total_occur - A
        C = n_label - A
        D = N - A - B - C
        chi_value = (float(N**2) * ((A*D - B*C)**2)) / \
                    ((A + C) * (A + B) * (B + D) * (B + C))
        # print "%f\t%s\t%s"%(chi_value, label, w)
        res.append((w, chi_value))
    res = sorted(res, key = lambda x : x[1], reverse = True)
    res_per_category[label] = res[:topK]

  logging.info("processing X-chi test done")
  return res_per_category


def ReadFile(fileName):
  f = open(fileName)
  content = f.readlines()
  f.close()
  li = []
  for line in content:
    line = line.strip()
    li.append(line)
  return li

def FeatureSelectForGiveData(remove_word_set):

  Y, X = [], []
  logging.info("read file done")
  for line in sys.stdin:
    line = line.rstrip()
    line = line.split("\t")
    Y.append(line[0])
    # append each word
    tmp = []
    for w in line[2:]:
      tokens = w.split()
      if len(tokens) == 2 and tokens[0] not in remove_word_set:
        tmp.append(tokens[0])
      else:
        logging.warn("error token format %s"% w)

    X.append(tmp)

  logging.info("start chi square test")
  if len(Y) != len(X):
    logging.error("len(Y) = %d, len(X) = %d"%(len(Y), len(X)))
    exit(-1)
  category_map = ChiSquareTest(Y, X, 3, 10000)
  for (label, v) in category_map.items():
    for x in v:
      print "%s %s %f"%(label, x[0], x[1])


def main():
  content = ReadFile("../data/remove_word.txt")
  remove_word = set(content)
  FeatureSelectForGiveData(remove_word)

if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format="""%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s""",
      datefmt='%Y-%H:%M:%S')
  main()
