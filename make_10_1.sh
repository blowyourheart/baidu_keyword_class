#!/bin/bash
# 这个脚本文件是用来对地域歧义词训练crf模型的，对训练数据进行10折以后
# 取出一份进行测试，来获得准确率和召回率的结果。

train_percent="0.9"
umask 077
tmp_dir="/tmp/classify"
all_data="$tmp_dir/all_data"

original_data="keyword_class.svm.label"
train_data="keyword_class.svm.train"
test_data="keyword_class.svm.test"

rm -rf $tmp_dir
mkdir -p $tmp_dir
# 去除注释和空行
cat -s $original_data | grep -v -P "^\s*$" | grep -v -P "^\s*#" | shuf > $all_data
line_num=`wc -l $all_data | awk '{print $1}'`
train_num=`python -c "print int($line_num * $train_percent)"`
# 抽样一定的百分比数据进行训练和测试
head -n $train_num $all_data > $train_data
tail -n $((line_num - train_num)) $all_data > $test_data
