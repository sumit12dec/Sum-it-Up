#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
import logging,json
import string
from flask import Flask, render_template, request, jsonify
stop_words = stopwords.words('english')

# The low end of shared words to consider
LOWER_BOUND = .20

# The high end, since anything above this is probably SEO garbage or a
# duplicate sentence
UPPER_BOUND = .90


def is_unimportant(word):
    """Decides if a word is ok to toss out for the sentence comparisons"""
    return word in ['.', '!', ',', ] or '\'' in word or word in stop_words


def only_important(sent):
    """Just a little wrapper to filter on is_unimportant"""
    return filter(lambda w: not is_unimportant(w), sent)


def compare_sents(sent1, sent2):
    """Compare two word-tokenized sentences for shared words"""
    if not len(sent1) or not len(sent2):
        return 0
    return len(set(only_important(sent1)) & set(only_important(sent2))) / ((len(sent1) + len(sent2)) / 2.0)


def compare_sents_bounded(sent1, sent2):
    """If the result of compare_sents is not between LOWER_BOUND and
    UPPER_BOUND, it returns 0 instead, so outliers don't mess with the sum"""
    cmpd = compare_sents(sent1, sent2)
    if cmpd <= LOWER_BOUND or cmpd >= UPPER_BOUND:
        return 0
    return cmpd


def compute_score(sent, sents):
    """Computes the average score of sent vs the other sentences (the result of
    sent vs itself isn't counted because it's 1, and that's above
    UPPER_BOUND)"""
    #logging.warning(sent)
    if not len(sent):
        return 0
    return sum(compare_sents_bounded(sent, sent1) for sent1 in sents) / float(len(sents))


def summarize_block(block):
    """Return the sentence that best summarizes block"""
    #logging.warning(block)
    import heapq
    if not block:
        return None
    sents = nltk.sent_tokenize(block)
    #logging.warning(sents)
    word_sents = map(nltk.word_tokenize, sents)
    #logging.warning(word_sents)
    d = dict((compute_score(word_sent, word_sents), sent) for sent, word_sent in zip(sents, word_sents))
    main_sum = d[d.keys()[d.values().index(sents[0])]]
    logging.warning(main_sum)
    key = d.keys()[d.values().index(sents[0])]+2
    d[key]=main_sum
    #logging.warning(d.keys()[d.values().index(sents[0])])
    #logging.warning("-------------------------")
    #logging.warning(d)
    if len(d)>=2:
    	two_maxs=heapq.nlargest(2,d.keys())
    	return d[two_maxs[0]]+d[two_maxs[1]]
    else:
    	return d[max(d.keys())]

def find_likely_body(b):
    """Find the tag with the most directly-descended <p> tags"""
    return max(b.find_all(), key=lambda t: len(t.find_all('p',recursive=False)))


class Summary(object):
    def __init__(self, url, article_html, title, summaries):
        self.url = url
        self.article_html = article_html
        self.title = title
        self.summaries = summaries
    
    def __repr__(self):
        return 'Summary({0}, {1}, {2}, {3})'.format(
            repr(self.url), repr(self.article_html), repr(self.title), repr(self.summaries)
        )

    def __str__(self):
        return u"Title: {0} <br/>Url: <a style='color:red;' href={1}>{1}</a><br/><br/>Summed Up:<br/>{2}<br><p style='float:right;color:rgb(86, 197, 51);font-size:11px;'>Report: <a style='color:rgb(86, 197, 51);' href='mailto:report@sumitraj.in' target='_blank';>report@sumitraj.in</a></p><p style='color:black;'>Placeholder</p>".format(self.title, self.url, '\n'.join(self.summaries))
    
    def cal(self):

        #return u"{0} - {1}\n\n{2}".format(self.title, self.url, '\n'.join(self.summaries))
#	self.res[0]['summary'] = self.res[0]['summary'].encode('utf-8')
	#print self.res[0]['summary']
        ss = "\n".join(self.summaries)
        res = {'url': self.url, 'title':self.title, 'summary':ss.encode('utf-8')}
        json.dumps(res)
        #res['summary'] = res['summary'].encode('utf8')
        #logging.warning(ss)
        return res

def summarize_page(url):
    import bs4
    import re
    import requests

    html = bs4.BeautifulSoup(requests.get(url).text)
    #logging.warning(html)
    b = find_likely_body(html)
    #logging.warning(b)
    summaries = map(lambda p: re.sub('\s+', ' ', summarize_block(p.text) or '').strip(), b.find_all('p'))
    #logging.warning(html.find_all('div','Normal'))
    if "timesofindia" in url :
        summaries = map(lambda div: re.sub('\s+', ' ', summarize_block(div.text) or '').strip(), html.find_all('div','Normal'))
    #logging.warning(b.find_all('div','Normal'))
    summaries = sorted(set(summaries), key=summaries.index)  # deduplicate and preserve order
    summaries = [re.sub('\s+', ' ', summary.strip())
                 for summary in summaries
                 if filter(lambda c: c.lower() in string.letters, summary)]
    print(summaries)
    return  Summary(url, b, html.title.text if html.title else None, summaries[:1])

def main1(sent_url):
        return  u"%s" % summarize_page(sent_url)
