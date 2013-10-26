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

  #read query title
  query_category = {}
  f = open(sys.argv[2])
  for line in f:
    line = line.rstrip()
    tokens = line.split("\t")
    query, category = tokens[0], tokens[1]
    query_category[query] = category
  f.close()
  logging.info("read %d query-category pair"%(len(query_category)))

  # read keyword_title.txt results
  # output the filter and merged info to target file
  f = open(sys.argv[1])
  fout = open(sys.argv[3], 'w')
  query_has_title = set()
  write_cnt = 0
  for line in f:
    line = line.rstrip()
    tokens = line.split("\t")
    query = tokens[0]
    tmp_set = set([ FilterGarbageTailingText(x) for x in tokens[1:]])
    if query not in query_category:
      logging.debug("%s not in keyword_class.txt"%query)
      continue
    else:
      fout.write("%s\t%s\n"%(query_category[query], line))
      query_has_title.add(query)
      write_cnt += 1
  f.close()
  logging.info("join query_title done, write total %d"%write_cnt)


  # output the query has no title
  unique_cnt = 0
  for (query, category) in query_category.iteritems():
    if query not in query_has_title:
      fout.write("%s\t%s\n"%(category, query))
      unique_cnt += 1
  logging.info("output %d unique query category"%(unique_cnt))
  fout.close()


if __name__ == "__main__":
  logging.basicConfig(
      level = logging.INFO,
      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
      datefmt='%Y-%H:%M:%S')
  main()
