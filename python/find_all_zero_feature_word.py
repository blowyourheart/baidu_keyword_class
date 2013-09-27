#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-25 16:56:30

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
  if len(sys.argv) != 3:
    logging.error("Usage: %s feature_uniq.txt weight_vector.txt"%(sys.argv[0]))
    exit(-1)

  feature_list = ReadFile(sys.argv[1])
  logging.info("feature size: %d", len(feature_list))

  weight_vec = ReadFile(sys.argv[2])
  logging.info("weight_vec size: %d"%(len(weight_vec)))
  null_idx = []
  pattern = re.compile(r"^[\s0]+$")
  for i in range(len(weight_vec)):
    if re.match(pattern, weight_vec[i]):
      # print weight_vec[i]
      print feature_list[i]


if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
