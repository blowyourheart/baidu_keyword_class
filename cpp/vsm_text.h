// Copyright 2012 Jike Inc. All Rights Reserved.
// Author: wangqun@jike.com(Wang Qun)
// Date  : 2012-11-07 18:46:36
// Brief : use segmenter to compute a sim hash result for a string

#ifndef VSM_TEXT_H_
#define VSM_TEXT_H_

#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#include <utility>
#include <iostream>

bool SkipCommentRead(const std::string& file_name, std::vector<std::string>* lines);

std::string Join(const std::vector<std::string>& vec, const std::string& sep);

void split(const std::string& src,
    const std::string& separator,
    std::vector<std::string>* dest);

std::string IntToString(int i);

/*
template<typename K, typename V>
std::ostream operator << (std::ostream& oss, const std::map<K, V>& kv) {
  typedef typename std::map<K, V>::const_iterator KVIT;
  oss << "{";
  for (KVIT it = kv.begin(); it != kv.end(); ++it) {
    oss << it->first << ":" << it->second << " ";
  }
  oss << "}";
  return oss;
}

template<typename K, typename V>
std::ostream operator << (std::ostream& oss, const std::pair<K, V>& pair) {
  oss << "(" << pair.first << "," << pair.second << ")";
  return oss;
}
*/

class VsmText {
  public:
    static const int kTokenSize = 30000;

    explicit VsmText(
        const std::vector<std::string>& include_tags);
    virtual ~VsmText();

    // the next two function should be called before GetWordPreqPair
    // return the number of stop words added in
    int AddStopWords(const std::string& filePath);

    // return true if @param word is added in, false otherwise
    bool AddSingleStopWord(const std::string& word);

    // seg text to <word tf idf>
    bool GetWordFreqPair(const std::string& text,
        std::map<std::string, std::pair<int, double> >* word_weight);

  private:
    std::set<std::string> includes_;
    std::set<std::string> stopWords_;  // NOLINT
    std::set<std::string> split_phrase_;
};

#endif
/* to be or not to be, that's the question. */
