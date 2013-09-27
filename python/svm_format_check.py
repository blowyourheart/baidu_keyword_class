#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-08-25 22:11:20

import sys
import os
import re
import logging

def RecordCheck(line):
  tokens = line.split()
  if len(tokens) <= 1:
    logging.error("%s no word"%line)
    return False

  #check label
  try:
    label = int(tokens[0])
  except Exception, e:
    logging.error("%s to int label error"%tokens[0])
    return False

  least_idx = -1
  for t in tokens[1:]:
    logging.debug("processing %s least_idx=%d"%(t, least_idx))
    pair = t.split(":")
    if len(pair) != 2:
      logging.error("%s token no pair"%t)
      return False

    idx = 0
    try:
      idx = int(pair[0])
    except Exception, e:
      logging.error("%s to int error"%pair[0])
      return False
    if idx <= least_idx:
      logging.error("%d <= prior idx: %d"%(idx, least_idx))
      return False
    else:
      least_idx = idx

    try:
      a = float(pair[1])
    except Exception , e:
      logging.error("convert float error %s"%pair[1])
      return False

  return True

def ReadFile(fileName):
  f = open(fileName)
  content = f.readlines()
  f.close()
  li = []
  for line in content:
    line = line.strip()
    li.append(line)
  return li

def main():
  line_cnt = 0
  for line in sys.stdin:
    line = line.rstrip()
    line_cnt += 1
    if RecordCheck(line) == False:
      logging.error("line %d format error"%line_cnt)
      exit(-1)

  logging.info("all %d records are valid"%line_cnt)

if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
