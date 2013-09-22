#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-22 17:32:17

import sys
import os
import logging
import re

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

replace_pattern = re.compile(r"(维基百科,自由|_百度|_互动|_搜搜).{,7}$")
def FilterGarbageTailingText(text):
  """
    remove the garbage title format such as 快速建筑设计50例_互动百科
    """
  return re.sub(replace_pattern, "", text)

def main():
  a = "../data/keyword_title.txt"
  b = "../data/keyword_class_unique.txt"
  c = "../data/merge_keyword_class_title.txt"
  if len(sys.argv) != 4:
    logging.error("Usage: %s %s %s %s"%(sys.argv[0], a, b, c))
    exit(-1)

  query_titles = {}
  f = open(sys.argv[1])
  for line in f:
    line = line.rstrip()
    tokens = line.split("\t")
    tmp_set = set([ FilterGarbageTailingText(x) for x in tokens[1:]])
    if tokens[0] not in query_titles:
      query_titles[tokens[0]] = tmp_set
    else:
      logging.warn("duplicate query %s"%(tokens[0]))
      query_titles[tokens[0]] |= tmp_set
  f.close()

  # read keyword_class_unique.txt results
  # output the filter and merged info to target file
  f = open(sys.argv[2])
  fout = open(sys.argv[3], 'w')
  for line in f:
    line = line.rstrip()
    tokens = line.split("\t")
    query, category = tokens[0], tokens[1]
    if query in query_titles:
      fout.write("%s\t%s\t%s\n"%(category, query, "\t".join(list(query_titles[query]))))
    else:
      fout.write("%s\t%s\n"%(category, query))
  f.close()
  fout.close()


if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
