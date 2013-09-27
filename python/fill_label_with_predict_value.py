#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-23 20:20:21
# Brife: 根据分类器预测的结果来填充整个keyword_class.txt的类标

import sys
import os
import re
import logging

def ReadFile(fileName):
  f = open(fileName)
  content = f.readlines()
  f.close()
  li = []
  for line in content:
    line = line.rstrip()
    if len(line) > 0:
      li.append(line)
  return li

def GetQueryCategory(label_file):
  content = ReadFile(label_file)
  query_category = {}
  for line in content:
    tokens = line.split("\t")
    if len(tokens) != 2:
      logging.error("format error %s"%line)
      exit(-2)
    query_category[tokens[0]] = tokens[1]

  return query_category

def main():
  if len(sys.argv) != 2:
    logging.error("Usage: %s predict.label.query < keyword_class_inner_unique.txt > keyword_class.predict.txt"%(sys.argv[0]))
    exit(-1)

  query_category = GetQueryCategory(sys.argv[1])
  logging.info("read query_category entry size : %d"%len(query_category))

  has_label, fill_label, default_label = 0, 0, 0
  for line in sys.stdin:
    line = line.rstrip()
    tokens = line.split("\t")
    if len(tokens) != 2:
      logging.error("format error %s"%line)
      exit(-3)
    if tokens[1] != '-':
      print line
      has_label += 1
    elif tokens[0] in query_category:
      print "%s\t%s"%(tokens[0], query_category[tokens[0]])
      fill_label += 1
    else:
      print "%s\t8"%(tokens[0])
      default_label += 1

  logging.info("job done has_label:%d, fill_label:%d, default_label:%d"%(has_label, fill_label, default_label))


if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
