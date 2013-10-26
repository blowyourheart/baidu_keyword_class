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

#include "vsm_text.h"

using namespace std; // NOLINT

void EXPECT_TRUE(bool flag) {
  if (!flag) {
    cerr << "error"
      << endl;
    exit(1);
  }
}

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

void PrintMap(const map<string, pair<int, double> >& data) {
  typedef map<string, pair<int, double> >::const_iterator KVIT;
  cout << "{";
  for (KVIT it = data.begin(); it != data.end(); ++it) {
    cout
      << it->first
      << ":"
      << "(" << it->second.first << "," << it->second.second << ")";
  }
  cout << "}" << endl;
}

int main(int argc, char* argv[]) {
  string tag[] = {
    "n", "s", "f", "v", "a", "z", "d"
  };
  vector<string> tags(tag, tag + sizeof(tag) / sizeof(tag[0]));
  VsmText vsm(tags);
  string a = "北京双井地区家乐福突发大火，起火原因尚不明确, 住酒店公寓";
  string b = "双井家乐福，大火之后你又出事了！";
  map<string, pair<int, double> > word_weight;
  map<string, pair<int, double> > word_weight2;

  EXPECT_TRUE(vsm.GetWordFreqPair(a, &word_weight));
  EXPECT_TRUE(vsm.GetWordFreqPair(b, &word_weight2));
  cout << a << endl;
  PrintMap(word_weight);

  cout << b << endl;
  PrintMap(word_weight2);
}
