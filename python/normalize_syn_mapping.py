#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-23 10:56:06

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

def main():
  if len(sys.argv) != 2:
    logging.error("Usage: %s ../syn.pair"%(sys.argv[0]))
    exit(-1)

  content = ReadFile(sys.argv[1])
  syn_map = {}
  for line in content:
    tokens = line.split("\t")
    if len(tokens) != 2:
      logging.error("error format %s"%line)
    else:
      syn_map[tokens[0]] = tokens[1]

  # remove unnecessary mapping pair
  final_syn = {}
  for (k, v) in syn_map.items():
    if v not in syn_map:
      final_syn[k] = v
    else:
      # select the shorter token as the target value
      if len(k) >= len(v):
        final_syn[k] = v
        if v in final_syn:
          del final_syn[v]
      else:
        final_syn[v] = k
        if k in final_syn:
          del final_syn[k]

  for (k, v) in final_syn.items():
    print "%s\t%s"%(k, v)

if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
