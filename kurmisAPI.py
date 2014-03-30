import urllib2
import time
from BeautifulSoup import BeautifulSoup
import pdb

def getWord(word):
    url = str.join('', ("http://www.sig.lt/linas/lt_form/?uzklausa=", word.encode('iso-8859-1'),  "&submit=Ie%F0koti"))
    try:
        response = urllib2.urlopen(url)
    except urllib2.URLError:
        time.sleep(10)
        response = urllib2.urlopen(url)
    html = response.read()
    parsed_html = BeautifulSoup(html)
    try:
        return parsed_html.body.findAll('b')[1].text
    except IndexError:
        return u'NA'


dic = open("dictionary.csv")
stemmed = []
for word in dic:
    print word
    word = word.replace("\n","").replace("\"","")
    #pdb.set_trace()
    stemmed.append(getWord(word))

dic.close()