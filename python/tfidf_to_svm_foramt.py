#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-08-25 18:16:38
# 将词的词频以及idf值做成一个个的特征向量，
# id  类标 特证词：权重

import sys
import os
import logging

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
    if len(j) != 3:
      logging.error("field format error: %s\n"%(i))
      continue
    if j[0] not in selected_words:
      logging.debug("%s not in the selected_words"%(j[0]))
      continue
    res.append([selected_words[j[0]], int(j[1])])
  return res

def NormalizeVec(a):
  res = []

  total_tf = 0.0
  for i in a:
    total_tf += i[1]
  total_weight = 0.0

  for i in a:
    tf = i[1] / total_tf
    tfidf = tf * i[2]
    total_weight += tfidf**2
    res.append([i[0], tfidf])

  total_weigth = total_weight ** 0.5

  for i in res:
    i[1] /= total_weight

  return res

def Vec2String(vec):
  res = []
  for i in vec:
    res.append(":".join([str(s) for s in i ]))
  return "\t".join(res)

def main():
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  content = ReadFile("./keyword_class.train")

  total_words = ReadFile("./feature_word.txt")
  i = 1
  select_words = {}
  for word in total_words:
    select_words[word] = i
    i += 1
  logging.info("select_words size: %d"%(len(select_words)))

  for line in content:
    line = line.strip()
    tokens = line.split('\t')
    if len(tokens) <= 2:
      logging.error("record format error %s\n"%line)
      continue
    vec = tokens[2:]
    vec = StringToVecList(vec, select_words)
    # vec = NormalizeVec(vec)
    print "%s\t%s"%(tokens[1], Vec2String(vec))


if __name__ == "__main__":
  main()
