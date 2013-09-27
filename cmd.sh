#!/bin/bash
# author: wangqun@jike.com
# created on 2013-09-23 13:51:33

seg_tf_cmd="
cat data/merge_keyword_class_title.txt | 
      ./to_vsm 
      --release_yrdata_prefix=/home/wangqun/jike/newproduct-coding 
      --segmenter_version=20120401 
      --segmenter_pool_size=1000 > data/merge_keyword_class_title.tf 2>data/merge_err.log
"

convert_to_svm_format="
./tfidf_to_svm_foramt.py > ../data/merge_keyword_class_title.tf.label.svm
"
