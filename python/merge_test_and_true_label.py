#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-23 17:32:34

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
  a = "../data/test.merge_keyword_class_title.tf.label.category"
  b = "../data/test.result.s6"
  if len(sys.argv) != 3:
    logging.error("Usage: %s %s %s > output_label"%(sys.argv[0], a, b))
    exit(-1)

  true_label = ReadFile(sys.argv[1])
  predict_label = ReadFile(sys.argv[2])
  if len(true_label) != len(predict_label):
    logging.error("len(true_label): %d != len(predict_label):%d"%(len(true_label), len(predict_label)))
    exit(-2)
  for i in range(len(true_label)):
    print "%s\t%s"%(true_label[i], predict_label[i])


if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
