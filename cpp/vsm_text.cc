// Copyright 2012 Jike Inc. All Rights Reserved.
// Author: wangqun@jike.com(Wang Qun)
// Date  : 2012-11-07 18:58:51
// Brief : implements

#include "vsm_text.h"
#include <fstream>
#include <iostream>
#include "ICTCLAS50.h"

using namespace std;

bool SkipCommentRead(const string& file_name, vector<string>* lines) {
  ifstream a(file_name.data());
  // a.open(file_name);
  if (!a) {
    return false;
  }
  string line;
  while (getline(a, line)) {
    lines->push_back(line);
  }
  return lines->empty();
}

string Join(const vector<string>& vec, const string& sep) {
  string res = "";
  for (size_t i = 0; i < vec.size(); i++) {
    res.append(vec[i]);
    if (i < vec.size() - 1) {
      res.append(sep);
    }
  }
  return res;
}

void split(const string& src, const string& separator, vector<string>* dest) {
  string str = src;
  string substring;
  string::size_type start = 0, index;
  do {
    index = str.find_first_of(separator,start);
    if (index != string::npos) {    
      substring = str.substr(start,index-start);
      dest->push_back(substring);
      start = str.find_first_not_of(separator,index);
      if (start == string::npos) {
        return;
      }
    }
  }while(index != string::npos);

  //the last token
  substring = str.substr(start);
  dest->push_back(substring);
}

std::string IntToString(int i) {
  char tmp[50];
  sprintf(tmp, "%d", i);
  return string(tmp);
}


VsmText::VsmText(const vector<string> &include_tags) {
  includes_.insert(include_tags.begin(), include_tags.end());

	if(!ICTCLAS_Init()) {
    //初始化分词组件。
		cerr << "Init fails\n";
		exit(1) ;
	} else {
		cerr << "Init ok\n";
	}

   //设置词性标注集(0 计算所二级标注集，1 计算所一级标注集，2 北大二级标注集，3 北大一级标注集)
	ICTCLAS_SetPOSmap(1);
}

VsmText::~VsmText() {
	ICTCLAS_Exit();	//释放资源退出
  cerr << "destructor VsmText success \n";
}

namespace {
bool only_digits(const string& input) {
  for (size_t i = 0; i < input.size(); i++) {
    if (!isdigit(input[i])) {
      return false;
    }
  }
  return true;
}
}


bool VsmText::GetWordFreqPair(const string& input,
    map<string, pair<int, double> >* word_weight) {
  if (input.empty()) {
    return true;
  }

  int nResultCount = 0;
	LPICTCLAS_RESULT pResult = ICTCLAS_ParagraphProcessA(
      input.data(),
      input.size(),
      nResultCount,
      CODE_TYPE_UTF8,
      1); 

  // output simple word weight
  for (int i = 0; i < nResultCount; i++) {
    const LPICTCLAS_RESULT pToken = pResult + i;
    string word = input.substr(pToken->iStartPos,
        pToken->iLength);
    string postag = pToken->szPOS;
    if (stopWords_.find(word) != stopWords_.end() ||
        includes_.find(postag) == includes_.end()||
        only_digits(word)) {
      // VLOG(20) << "ignore " << token.word_;
      continue;
    }
    double idf = 10;
    idf = pToken->iWeight;
    map<string, pair<int, double> >::iterator mit;
    mit = word_weight->find(word);
    if (mit == word_weight->end()) {
      word_weight->insert(make_pair(word, make_pair(1, idf)));
    } else {
      mit->second.first++;
    }
  }
  {
    // using namespace social_mining::region_identify;  NOLINT
    // VLOG(20) << "word_weight: " << *word_weight;
  }

  ICTCLAS_ResultFree(pResult);
  return !word_weight->empty();
}

bool VsmText::AddSingleStopWord(const string &word) {
  return stopWords_.insert(word).second;
}

int VsmText::AddStopWords(const string &file) {
  vector<string> values;
  if (!SkipCommentRead(file, &values)) {
    cerr << " load file error: " << file
      << endl;
  }
  int count = 0;
  for (size_t i = 0; i < values.size(); i++) {
    if (AddSingleStopWord(values[i])) {
      count++;
    }
  }
  cerr << "add " << count << " words from " << file
    << endl;
  return count;
}
