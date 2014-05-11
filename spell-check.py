# -*- coding: utf-8 -*-

__author__ = 'e.dunajevas'

import enchant
import re
import pandas as pd
import pdb
def suggest_lt(word):
    """
    suggests lithuanian word correction
    @param word: single sting
    @return: corrected word
    """
    d = enchant.Dict("lt_LT")
    if d.check(word):
        return(word)
    else:
        if word[0] == 'w':
            word = 'v' + word[1:]
        if word[0] == 'x':
            word = "ch" + word[1:]
        if word[0] == '2' and len(word) != 1:
            word = "du" + word[1:]
        out = d.suggest(word)
        if len(out) == 0:
            return(word)
        else:
            return(out[0])

comments = pd.read_csv('data/comments.csv', encoding='utf8')

for i in range(1, 1000):
    print i
    print comments['CommentText'][i]
    sentence = re.sub(u"[^a-zA-Z0-9ą-žĄ-Ž]+", ' ', comments['CommentText'][i])
    print sentence
    out = ''
    for word in sentence.strip(' \t\n\r').split(" "):
        out.join(suggest_lt(word))
    print out
