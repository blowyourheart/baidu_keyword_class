#!/bin/bash
# author: wangqun@jike.com
# created on 2013-08-28 17:13:12

for i in `seq 1 10`
do
  echo process circle $i
  ./make_10_1_sogou.sh
  ./nb.py 2>/dev/null > sogou.test.result
  ./confusion_matrix.py < sogou.test.result
done
