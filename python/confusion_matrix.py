#!/usr/bin/env python
# coding: utf-8
# Copyright 2012 JIKE.COM ALL Rights Reserved.
# Author: wangqun@jike.com
# created on 2013-08-26 14:54:49

import sys
import os
from collections import defaultdict


show_matrix = False
show_percent = False

def FormatList(vec_list, least_num_space = 2):
  max_word_len = 0
  num_elements_per_line = max([len(x) for x in vec_list])
  for i in vec_list:
    for j in i:
      max_word_len = max(max_word_len, len(j))

  line_size = max_word_len * num_elements_per_line + \
              least_num_space * (num_elements_per_line - 1)
  res = []
  for x in vec_list:
    string = ""
    for i in range(0, len(x)):
      string += x[i]
      expect_len = max_word_len * (i + 1) + 2 * (i + 1)
      string += " " * (expect_len - len(string))
    res.append(string)
  print "\n".join(res)


def main():
  matrix = defaultdict(int)
  all_label = defaultdict(int)
  total_doc = 0
  total_right = 0

  for line in sys.stdin:
    line = line.strip()
    tokens = line.split()
    original_label, predict_label = tokens[-2], tokens[-1]

    total_doc += 1
    if original_label == predict_label:
      total_right += 1

    all_label[original_label] += 1

    key = "%s %s"%(original_label, predict_label)
    matrix[key] += 1

  #compute precise for total, avg, and individual_precise
  print "total precise: %.3f"%(float(total_right) / total_doc)
  individual_precise = []
  avg_precise = 0.0
  for (label, cnt) in all_label.items():
    key = "%s %s"%(label, label)
    cur_precise = float(matrix[key]) / cnt
    avg_precise += cur_precise
    # individual_precise[label] = cur_precise
    individual_precise.append((label, cur_precise))
  avg_precise /= len(individual_precise)
  print "avg_precise: %.3f"%avg_precise
  individual_precise = sorted(individual_precise, key = lambda x:x[1])
  print "\n".join(["%s\t%.3f"%(k,v) for (k, v) in individual_precise])
    
  if not show_matrix:
    return

  # output the confusion matrix
  all_vec =  [[ k for (k, v) in all_label.items()]]
  vec= []
  for a, va in all_label.items():
    vec = []
    for b, vb in all_label.items():
      key = "%s %s"%(a, b)
      v = "0"
      if key in matrix:
        if show_percent:
          v = "%.2f"%(float(matrix[key]) / va)
        else:
          v = matrix[key]

      vec.append(v)
    vec.append(a)
    all_vec.append([str(x) for x in vec])

  FormatList(all_vec, 2)

if __name__ == "__main__":
  main()
