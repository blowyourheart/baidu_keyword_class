#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-14 12:24:57

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
  line = line.strip()
  word, count = line.split('\t', 1)
  try:
    count = int(count)
  except ValueError:
    continue

  if current_word == word:
    current_count += count
  else:
    if current_word:
      print '%s\t%s' % (current_word, current_count)
      current_count = count
      current_word = word
    else:
      current_word, current_count = word, 1

# do not forget to output the last word if needed!
if current_word == word:
  print '%s\t%s' % (current_word, current_count)
