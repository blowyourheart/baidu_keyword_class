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

#include "vsm_text.h"

using namespace std;  // NOLINT

VsmText* VSM;

void ProcessAQuery(const string& query, string* to) {
  map<string, pair<int, double> > result;
  // VLOG(1) << "content: " << query;
  VSM->GetWordFreqPair(query, &result);

  vector<string> output;
  map<string, pair<int, double> >::const_iterator it;
  for (it = result.begin(); it != result.end(); ++it) {
    string tuple = it->first;
    tuple.append(" ");
    tuple.append(IntToString(it->second.first));
    // tuple.append(" ");
    // tuple.append(DoubleToString(it->second.second));
    output.push_back(tuple);
  }
  *to = Join(output, "\t");
}


int main(int argc, char** argv) {
  string tag[] = {
    "n", "s", "f", "v", "a", "z", "d"
  };
  vector<string> tags(tag, tag + sizeof(tag) / sizeof(tag[0]));
  VsmText vsm(tags);
  VSM = &vsm;
  string line;
  while (getline(cin, line)) {
    vector<string> tokens;
    split(line, "\t", &tokens);
    if (tokens.size() < 2) {
      cerr << " tokens size < 2" << endl;
      exit(2);
    }
    const string& label = tokens[0];
    const string& query = tokens[1];
    size_t idx = line.find('\t');
    const string query_title = line.substr(idx + 1);
    string vsm;
    ProcessAQuery(query_title, &vsm);
    if (vsm.empty()) {
      cerr
        << query << "\thas no feature"
        << endl;
    } else {
      cout
        << label << '\t'
        << query << '\t'
        << vsm
        << endl;
    }
  }

  return 0;
}
