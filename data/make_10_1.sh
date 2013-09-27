#!/bin/bash
# 这个脚本文件是用来对地域歧义词训练crf模型的，对训练数据进行10折以后
# 取出一份进行测试，来获得准确率和召回率的结果。

train_percent="0.9"
umask 077
tmp_dir="/tmp/classify"
all_data="$tmp_dir/all_data"

original_data="merge_keyword_class_title.tf.label.svm"
train_data="train.merge_keyword_class_title.tf.label.svm"
test_data="test.merge_keyword_class_title.tf.label.svm"

rm -rf $tmp_dir
mkdir -p $tmp_dir
# 去除注释和空行
cat  $original_data |  shuf > $all_data
line_num=`wc -l $all_data | awk '{print $1}'`
train_num=`python -c "print int($line_num * $train_percent)"`
echo line_num: $line_num   train_num: $train_num
# 抽样一定的百分比数据进行训练和测试
head -n $train_num $all_data > $train_data
tail -n $((line_num - train_num)) $all_data > $test_data
