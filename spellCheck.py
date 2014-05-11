# -*- coding: utf-8 -*-

__author__ = 'e.dunajevas'

import re
import pandas as pd
from correctDidYouMean import correct

def correct_base(word):
    #obvious corrections
    word = word.lower()
    word = re.sub('w', 'v', word)
    word = re.sub('x', 'ch', word)
    word = re.sub('2', 'du', word)
    #removes double characters like tooooks -> toks
    word = re.sub(r'([a-z])\1+', r'\1', word)
    return correct(word)

comments = pd.read_csv('data/comments.csv', encoding='utf-8')
#import correctDidYouMean
#correctDidYouMean.known(['pakaisioji'])
for i in range(15, 16):
    print i
    sentence = re.sub(u"[^a-zA-Z0-9ą-žĄ-Ž]+", ' ', comments['CommentText'][i])
    print sentence
    out = []
    for word in sentence.strip(' \t\n\r').split(" "):
        out.append(correct_base(word))
    #print " ".join(out)
