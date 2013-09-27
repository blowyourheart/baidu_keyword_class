// Copyright 2012 Jike Inc. All Rights Reserved.
// Author: wangqun@jike.com(Wang Qun)
// Date  : 2012-11-07 18:58:51
// Brief : implements

#include "base/scoped_ptr.h"
#include "base/string_util.h"
#include "base/yr.h"
#include "bi/social_mining/weibo/baidu/vsm_text.h"
#include "bi/social_mining/weibo/public/zone_detect/region_util.h"
#include "util/re2/re2.h"
#include "util/segmenter/public/segmenter.h"
#include "util/segmenter/word_idf/word_idf_dict.h"


using social_mining::region_identify::SkipCommentRead;
using social_mining::region_identify::Join;
using segmenter::WordIDFDictionary;
using segmenter::WordIDFDictFactory;
using segmenter::TokenTypeEnum;
using segmenter::SegmentedToken;

namespace social_mining {

VsmText::VsmText(const vector<segmenter::TokenTypeEnum> &includes) {
  includes_.insert(includes.begin(), includes.end());

  tokens_.reset(new SegmentedToken[kTokenSize]);
  CHECK(tokens_.get()) << "new SegmentedToken array error";

  vector<string> contents;
  CHECK(SkipCommentRead("./split_phrase.txt", &contents));
  CHECK_GT(contents.size(), 0);
  hash_set<string> tmp(contents.begin(), contents.end());
  split_phrase_.swap(tmp);
  LOG(INFO) << "load " << split_phrase_.size()
    << " split_phrase";
}

namespace {
bool FilterSemanticAttribute(const nlp::SemanticAttribute& attr) {
  return attr.puctuation ||
    // attr.place_name ||
    attr.stopword;
}

bool DoNotSplitPhase(const nlp::SemanticAttribute& attr) {
  return attr.people_name ||
    attr.organization ||
    attr.idom ||
    attr.weak_idom ||
    attr.proper_noun;
}
}

VsmText::~VsmText() {
  LOG(INFO) << "destructor VsmText success";
}

bool VsmText::GetWordFreqPair(const string& input,
    map<string, pair<int, double> >* word_weight) {
  scoped_ptr<segmenter::Segmenter> segmenter;
  segmenter.reset(segmenter::SegmenterManager::GetSegmenter());
  if (segmenter == NULL) {
    return false;
  }
  segmenter->Init();
  segmenter->set_upper2lower(true);
  segmenter->set_compress_punct(true);
  segmenter->set_join_english_digit(true);
  segmenter->set_compress_space_like(true);
  segmenter->set_full2half_width(true);
  segmenter->set_non_display_as_space(true);
  segmenter->set_deref_html_entity(true);

  segmenter->FeedText(input.data(), input.size());
  int len = 0;
  while (segmenter->GetNextToken(&tokens_[len])) {
    if (tokens_[len].is_phrase()) {
      bool should_split = false;
      if (utflen(tokens_[len].word_.data()) >= 4 &&
          !DoNotSplitPhase(tokens_[len].semantic_attribute_)) {
        should_split = true;
        VLOG(2) << "split phase longer than 4: " << tokens_[len].word_;
      }
      if (!should_split && 
         split_phrase_.find(tokens_[len].word_) != split_phrase_.end()) {
        should_split = true;
        VLOG(2) << "in split dict: " << tokens_[len].word_;
      }
      if (!should_split) {
        VLOG(2) << "donot split phrase: " << tokens_[len].word_;
        VLOG(20) << "adding " << tokens_[len].word_
          << " len size: " << len;
        len++;
      } else {
        segmenter::SegmentedToken subTokens[100];
        int subCount = segmenter->GetSubTokens(tokens_[len], false, subTokens,
            arraysize(subTokens));
        for (int i = 0; i < subCount; i++) {
          tokens_[len] = subTokens[i];
          VLOG(20) << "adding " << tokens_[len].word_
            << " len size: " << len;
          len++;
        }
      }
    } else {
      VLOG(20) << "adding " << tokens_[len].word_
        << " len size: " << len;
      len++;
    }
  }  // end segmenter sentence

  VLOG(20) << "after segmenter";

  WordIDFDictionary* idf_dict =
    Singleton<WordIDFDictFactory>::get()->GetDict(FLAGS_segmenter_version);
  static RE2 ONLY_DIGITS("\\d+");
  // output simple word weight
  for (int i = 0; i < len; i++) {
    const segmenter::SegmentedToken& token = tokens_[i];
    VLOG((20)) << token.word_ << " " << "[" << token.begin_
      << ", " << token.end_ << "]";
    if (stopWords_.find(token.word_) != stopWords_.end() ||
        includes_.find(token.type_) == includes_.end()||
        FilterSemanticAttribute(token.semantic_attribute_) ||
        RE2::FullMatch(token.word_, ONLY_DIGITS)) {
      VLOG(20) << "ignore " << token.word_;
      continue;
    }
    double idf = 10;
    idf_dict->GetIDFLogValue(token.word_, &idf);
    map<string, pair<int, double> >::iterator mit;
    mit = word_weight->find(token.word_);
    if (mit == word_weight->end()) {
      word_weight->insert(make_pair(token.word_, make_pair(1, idf)));
    } else {
      mit->second.first++;
    }
  }
  {
    using namespace social_mining::region_identify;  // NOLINT
    VLOG(20) << "word_weight: " << *word_weight;
  }

  return !word_weight->empty();
}

bool VsmText::AddSingleStopWord(const string &word) {
  return stopWords_.insert(word).second;
}

int VsmText::AddStopWords(const string &file) {
  vector<string> values;
  CHECK(SkipCommentRead(file, &values))
    << " load file error: " << file;
  int count = 0;
  for (int i = 0; i < values.size(); i++) {
    if (AddSingleStopWord(values[i])) {
      count++;
    }
  }
  LOG(INFO) << "add " << count << " words from " << file;
  return count;
}

}  // namespace social_mining
