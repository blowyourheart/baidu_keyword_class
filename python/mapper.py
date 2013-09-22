#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-09-14 12:22:31

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
  line = line.strip()
  words = line.split()
  # increase counters
  for word in words:
    print '%s\t1' % (word)
