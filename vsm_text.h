// Copyright 2012 Jike Inc. All Rights Reserved.
// Author: wangqun@jike.com(Wang Qun)
// Date  : 2012-11-07 18:46:36
// Brief : use segmenter to compute a sim hash result for a string

#ifndef BI_SOCIAL_MINING_WEIBO_PUBLIC_VSM_TEXT_H_
#define BI_SOCIAL_MINING_WEIBO_PUBLIC_VSM_TEXT_H_

#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#include <utility>

#include "base/hash_tables.h"
#include "base/scoped_ptr.h"
#include "util/simhash/simhash.h"
#include "util/segmenter/public/segmenter.h"

namespace social_mining {
class VsmText {
  public:
    static const int kTokenSize = 30000;

    explicit VsmText(
        const std::vector<segmenter::TokenTypeEnum>& includes);
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
    std::set<segmenter::TokenTypeEnum> includes_;
    base::hash_set<std::string> stopWords_;  // NOLINT
    base::hash_set<std::string> split_phrase_;
    scoped_array<segmenter::SegmentedToken> tokens_;

    DISALLOW_COPY_AND_ASSIGN(VsmText);
};

}  // namespace social_mining
#endif  // BI_SOCIAL_MINING_WEIBO_PUBLIC_VSM_TEXT_H_
/* to be or not to be, that's the question. */
