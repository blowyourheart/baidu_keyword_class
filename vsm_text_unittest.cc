// Copyright 2013 Jike Inc. All Rights Reserved.
// Author: wangqun@jike.com(Wang Qun)
// Date  : 2013-08-22 19:42:22
// Brief : simple_test.cc
#include <string>
#include <vector>
#include <set>
#include <map>
#include <algorithm>
#include <utility>
#include <iostream>  // NOLINT

#include "base/logging.h"
#include "base/string_util.h"
#include "base/scoped_ptr.h"
#include "base/singleton.h"
#include "base/flags.h"
#include "base/yr.h"

#include "bi/social_mining/weibo/public/zone_detect/region_util.h"
#include "bi/social_mining/weibo/baidu/vsm_text.h"

#include "testing/gtest/include/gtest/gtest.h"

using namespace social_mining;  // NOLINT
using namespace segmenter;  // NOLINT
using namespace social_mining::region_identify;  // NOLINT

namespace social_mining {

  struct ProgramTest : public testing::Test {
    ProgramTest()  { }
    ~ProgramTest() { }

    static void SetUpTestCase() {
    }
    static void TearDownCase() {
    }
    void SetUp() {
      // init data member here
      TokenTypeEnum e[] = {segmenter::TokenType::CJK_WORD,
        segmenter::TokenType::ENGLISH, segmenter::TokenType::DIGIT,
        segmenter::TokenType::PHRASE, segmenter::TokenType::POINT_DIGIT,
        segmenter::TokenType::FULLWIDTH_DIGIT};
      vector<TokenTypeEnum> v(e, e + arraysize(e));
      VsmText *simHash = new VsmText(v);
      vsm_.reset(simHash);
      CHECK(vsm_.get()) << "simHash init failed";
      string stopWords = social_mining::GetYrDataPath(
          "bi/social_mining/weibo/public/final_output/stopword_list");
      vsm_->AddStopWords(stopWords);
    }
    void TearDown() {
    }

    // data member here;
    scoped_ptr<VsmText> vsm_;
  };

  double CosSim(const map<string, double>& lhs,
      const map<string, double>& rhs) {
    typedef map<string, double>::const_iterator MSI;
    MSI ia = lhs.begin();
    MSI ib = rhs.begin();
    double res = 0;
    while (ia != lhs.end() && ib != rhs.end()) {
      if (ia->first < ib->first) {
        ++ia;
      } else if (ia->first > ib->first) {
        ++ib;
      } else {
        res += ia->second * ib->second;
        ++ia;
        ++ib;
      }
    }
    return res;
  }

  TEST_F(ProgramTest, GetWordFreqPair) {
    string a = "北京双井地区家乐福突发大火，起火原因尚不明确, 住酒店公寓";
    string b = "双井家乐福，大火之后你又出事了！";
    map<string, pair<int, double> > word_weight;
    map<string, pair<int, double> > word_weight2;

    EXPECT_TRUE(vsm_->GetWordFreqPair(a, &word_weight));
    EXPECT_TRUE(vsm_->GetWordFreqPair(b, &word_weight2));
    cout << a << endl
      << " word_weight: " << word_weight
      << endl;

    cout << b << endl
      << " word_weight: " << word_weight2
      << endl;

  }
}
