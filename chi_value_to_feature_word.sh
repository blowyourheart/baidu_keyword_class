#!/bin/bash
# author: wangqun@jike.com
# created on 2013-09-16 10:27:19

awk 'NF==3 {print $2}' feature_select.txt | sort -u > feature_word.txt
