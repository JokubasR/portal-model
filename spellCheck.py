
# -*- coding: utf-8 -*-

__author__ = 'e.dunajevas'

import re
import pandas as pd
#import pdb
#import distance
from correctDidYouMean import correct

def correct_base(word):
    #obvious corrections
    # pdb.set_trace()
    if word.isnumeric() or (word != u'į' and len(word) == 1):
        return word
    else:
        original = word
        word = word.lower()
        word = re.sub(u'w', u'v', word)
        word = re.sub(u'2', u'du', word)
        word = re.sub(u'sh', u'š', word)
        #removes double characters like tooooks -> toks
        word_wd = re.sub(ur'([a-ząčęęėįšųūž])\1+', r'\1', word)
        word = correct(word_wd)
        #if distance.levenshtein(word.lower()[0:5], word_wd.lower()[0:5]) > 2:
        #    word = u'\''+original+u'\''
        if original[0].isupper():
            word = word.title()
        if original.isupper():
            word = word.upper()
        return word

comments = pd.read_csv('data/commentsNEW.csv', encoding='utf-8')
comments['CommentTextChecked'] = 'NA'
for i in range(0, len(comments)):
#for i in range(23200, 23300):
    #if 0 == i % 100:
    print i
    try:
        sentence = re.sub(u"[^a-zA-Z0-9ą-žĄ-Ž]+", ' ', comments['CommentText'][i])
        sentence = re.sub(u"quot |quo ", "", sentence)
        out = []
        for word in sentence.strip(' \t\n\r').split(" "):
            #pdb.set_trace()
            out.append(correct_base(word))
        comments['CommentTextChecked'][i] = ' '.join(out)
    except (IndexError, TypeError) as err:
            comments['CommentTextChecked'][i] = 'NA'
comments.to_csv('comment_spellchecked.csv', encoding='utf8')
