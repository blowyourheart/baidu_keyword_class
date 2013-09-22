// Copyright 2013 Jike Inc. All Rights Reserved.
// Author: wangqun@jike.com(Wang Qun)
// Date  : 2013-08-25 17:08:43
// Brief : transform sogou text classify text to vsm


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
#include "base/yr.h"
#include "base/flags.h"
#include "base/at_exit.h"

#include "file/file.h"
#include "file/simple_line_reader.h"

#include "bi/social_mining/weibo/baidu/vsm_text.h"
#include "bi/social_mining/weibo/public/zone_detect/region_util.h"

using namespace social_mining;  // NOLINT
using namespace segmenter;  // NOLINT
using namespace social_mining::region_identify;  // NOLINT

base::AtExitManager atExit;
scoped_ptr<VsmText> VSM;

void ProcessAQuery(const string& query, string* to) {
  map<string, pair<int, double> > result;
  VLOG(1) << "content: " << query;
  VSM->GetWordFreqPair(query, &result);

  vector<string> output;
  map<string, pair<int, double> >::const_iterator it;
  for (it = result.begin(); it != result.end(); ++it) {
    string tuple = it->first;
    tuple.append(" ");
    tuple.append(IntToString(it->second.first));
    tuple.append(" ");
    tuple.append(DoubleToString(it->second.second));
    output.push_back(tuple);
  }
  *to = JoinString(output, "\t");
}


int main(int argc, char** argv) {
  base::ParseCommandLineFlags(&argc, &argv, true);
  {
    // init data member here
    TokenTypeEnum e[] = {segmenter::TokenType::CJK_WORD,
      segmenter::TokenType::ENGLISH, segmenter::TokenType::DIGIT,
      segmenter::TokenType::PHRASE, segmenter::TokenType::POINT_DIGIT,
      segmenter::TokenType::FULLWIDTH_DIGIT};
    vector<TokenTypeEnum> v(e, e + arraysize(e));
    VsmText *simHash = new VsmText(v);
    VSM.reset(simHash);
    CHECK(VSM.get()) << "simHash init failed";
    string stopWords = social_mining::GetYrDataPath(
        "bi/social_mining/weibo/public/final_output/stopword_list");
    VSM->AddStopWords(stopWords);
  }
  string line;
  while (getline(cin, line)) {
    vector<string> tokens;
    SplitString(line, '\t', &tokens);
    CHECK_EQ(2, tokens.size()) << " tokens size != 2";
    const string& query = tokens[0];
    const string& label = tokens[1];
    string vsm;
    ProcessAQuery(query, &vsm);
    if (vsm.empty()) {
      cerr
        << query << "\thas no feature"
        << endl;
    } else {
      cout
        << query << '\t'
        << label << '\t'
        << vsm
        << endl;
    }
  }

  return 0;
}
