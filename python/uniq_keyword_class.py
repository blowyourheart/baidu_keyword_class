#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-22 15:47:28

import sys
import os
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
  a = "../data/keyword_class.txt"
  b = "../data/keyword_class_unique.txt"
  c = "../data/keyword_class_inner_label.txt"
  if len(sys.argv) != 4:
    logging.error("Usage: %s %s %s %s"%(sys.argv[0], a, b, c))
    exit(-1)

  keyword_class = ReadFile(sys.argv[1])
  logging.debug("read file done")
  query_category = {}
  for line in keyword_class:
    tokens = line.split("\t")
    if len(tokens) != 2:
      logging.error("format error %s"%line)
      continue
    query, category = tokens[0], tokens[1]
    if query not in query_category:
      tmp = set()
      tmp.add(category)
      query_category[query] = tmp
    else:
      query_category[query].add(category)
  logging.debug("construct query_category map done")

  # check query_category valid
  for (query, category) in query_category.items():
    if len(category) > 1:
      category.discard('-')
    if len(category) > 1:
      logging.error("%s has more than 1 label: %s"%(query, ",".join(list(category))))
  logging.debug("check query_category valid done")

  # output unique query-category pair
  f = open(sys.argv[2], 'w')
  for (query, category) in query_category.items():
    a = list(category)
    f.write("%s\t%s\n"%(query, a[0]))
  f.close()
  logging.debug("write keyword_class_unique.txt done")

  # output inner-labeled query category
  f = open(sys.argv[3], 'w')
  for line in keyword_class:
    tokens = line.split("\t")
    if len(tokens) != 2:
      logging.error("format error %s"%line)
      continue
    query, category = tokens[0], tokens[1]
    a = list(query_category[query])
    f.write("%s\t%s\n"%(query, a[0]))
  logging.debug("write keyword_class_inner_label.txt done")

if __name__ == "__main__":
  logging.basicConfig(
      level = logging.DEBUG,
      #level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
