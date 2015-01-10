import bs4
import re
import sys
import nltk
import string
import urllib2
from collections import OrderedDict
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
def sum2(url):
    html = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    if 'usatoday' in url:
        main_text = re.sub('\s+',' '," ".join([ x.text for x in soup.find_all('p') ][14:]))
    elif 'gizmodo' in url:
        main_text = re.sub('\s+',' ',soup.find_all('div','Normal')[0].text)    
    elif 'thehindu' in url:
        articlelead = re.sub('\s+',' ',soup.find_all('div','articleLead')[0].text)
        main_text = re.sub('\s+',' '," ".join([ x.text for x in soup.find_all('p','body') ]))
    elif 'timesofindia' in url:
        if re.findall('<div class="Normal"',html):
            main_text = re.sub('\s+',' ',soup.find_all('div','Normal')[0].text)
        if re.findall('<div class="data"',html):
            main_text = re.sub('\s+',' ',soup.find_all('div','data')[0].text)
    else:
	main_text = re.sub('\s+',' '," ".join([ x.text for x in soup.find_all('p') ]))
    sents = nltk.sent_tokenize(main_text)
    words = map(nltk.word_tokenize,sents)
    title_words = map(string.lower,nltk.word_tokenize(soup.title.text))
    punc = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'] 

    sum = [ sents[words.index(x)] for x in words for y in x if string.lower(y) not in stop_words if string.lower(y) in title_words ]
    summary = list(OrderedDict.fromkeys(sum))
    if len(summary)>5:
        summary = " ".join(summary[0:5])
    else: summary = " ".join(summary)
    return u"Title: {0} <br/>Url: <a style='color:white;' target='_blank' href={1}>{1}</a><br/><br/>Summed Up:<br/>{2}<br><p style='float:right;color:white;font-size:11px;'>Report: <a style='color:white;' href='mailto:report@sumitraj.in?Subject={1}' target='_blank';>Help us Improve</a></p><p style='color:black;'>Placeholder</p>".format(soup.title.text,url, summary)

