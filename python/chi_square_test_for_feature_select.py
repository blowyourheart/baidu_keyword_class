#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-08-28 14:54:34

import sys
import os
import logging


# X: [label1 word0 word1 ...]
# topK: return the topK chi value per category
def ChiSquareTest(X, topK = 2000):
  N = len(X)
  category_cnt = {}
  word_label_cnt = {}

  for x in X:
    logging.debug("processing a record")
    label = x[0]
    if label in category_cnt:
      category_cnt[label] += 1
    else:
      category_cnt[label] = 1

    for w in x[1:]:
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

def FeatureSelectForGiveData(filename):
  content = ReadFile(filename)
  X = []
  logging.debug("read file done")
  for line in content:
    line = line.split("\t")
    tmp = [line[1]]
    for w in line[2:]:
      tokens = w.split()
      if len(tokens) == 3:
        tmp.append(tokens[0])
      else:
        logging.warn("error token format %s"% w)

    X.append(tmp)

  logging.debug("start chi square test")
  category_map = ChiSquareTest(X, 7000)
  for (label, v) in category_map.items():
    for x in v:
      print "%s %s %f"%(label, x[0], x[1])


def main():
  logging.basicConfig(level = logging.INFO)
  FeatureSelectForGiveData("keyword_class.train")

if __name__ == "__main__":
  main()
