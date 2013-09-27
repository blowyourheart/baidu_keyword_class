#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-08-25 18:16:38
# 将 词:tf 根据选出来的特征词做成 svm格式
# id  类标 特证词：权重

import sys
import os
import logging
import math

def ReadFile(fileName):
  f = open(fileName)
  content = f.readlines()
  f.close()
  li = []
  for line in content:
    line = line.strip()
    if len(line) > 0:
      li.append(line)
  return li

def StringToVecList(a, selected_words):
  res = []
  for i in a:
    j = i.split()
    if len(j) != 2:
      logging.error("field format error: %s\n"%(i))
      continue
    if j[0] not in selected_words:
      logging.debug("%s not in the selected_words"%(j[0]))
      continue
    res.append([selected_words[j[0]], int(j[1])])
    # logging.debug("convert %s to idx: %d"%(j[0], selected_words[j[0]]))
  # sort vec
  res = sorted(res, key = lambda x : x[0])
  return res

def NormalizeVec(a):
  "normalize via tf because of short text"

  total_tf = 0.0
  for i in a:
    total_tf += i[1]

  norm_weight = 0.0
  for i in a:
    i[1] /= total_tf
    norm_weight += i[1] * i[1]

  norm_weight = math.sqrt(norm_weight)
  # logging.debug("norm_weight= %f"%norm_weight)
  for i in a:
    i[1] = "%.4f"%(i[1] / norm_weight)

def Vec2String(vec):
  res = []
  for i in vec:
    res.append(":".join([str(s) for s in i ]))
  return "\t".join(res)

def main():
  feature_file = "../data/feature_uniq.txt"
  if len(sys.argv) != 2:
    logging.error("Usage: %s %s < input_tf.txt > output_svm.txt"%(sys.argv[0], a))
    exit(-1)
  total_words = ReadFile(sys.argv[1])
  i = 1
  select_words = {}
  for word in total_words:
    select_words[word] = i
    i += 1
  logging.info("select_words size: %d"%(len(select_words)))

  for line in sys.stdin:
    line = line.rstrip()
    tokens = line.split('\t')
    if len(tokens) <= 2:
      logging.error("record format error %s"%line)
      continue
    vec = tokens[2:]
    vec = StringToVecList(vec, select_words)
    NormalizeVec(vec)
    label = tokens[0]
    if label == '-':
      label = '8'
    print "%s\t%s"%(label, Vec2String(vec))

  logging.info("convert format done")


if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
