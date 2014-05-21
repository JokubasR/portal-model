
# coding=utf-8

# http://norvig.com/spell-correct.html
import re, collections
#import pdb
alphabet_all = u"aąbcčdeęėfghiįjklmnopqrsštuųūvwxyzž"
alphabet_lt = u"aącčeęėiįysšuųūzž"

def words(text):
    text = text.decode('utf-8')
    words = re.findall(u'[aąbcčdeęėfghiįjklmnopqrsštuųūvwxyzž]+', text.lower())
    #if words[0][0] == '\xbb' and words[0][1] == '\xbf':
    #    words[0] = words[0][2:]
    #return [w.decode('utf-8') for w in words]
    return words
#[w.decode('utf-8') for w in words[582:583]]

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

from_articles = words(file('dictionaries/dictionary.txt').read())
swear_words = words(file('dictionaries/swear-words.txt').read())
NWORDS = train(from_articles + swear_words)

ALPHA_LIST = []
for alpha in alphabet_lt:
    ALPHA_LIST.append(alpha)

def edits1(word, alphabet = alphabet_all):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def concat_lists(list1, list2):
    out = []
    for l1 in list1:
        for l2 in list2:
            out.append(l1 + l2)
    return out

def known_edits2(word):
    try:
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
    except:
        return set()

def editsLTx(word):
    return [re.sub('x', 'ks', word), re.sub('x', 'ch', word)]

def editsLT(word):
    letters = ['']
    for letter in word:
        if letter in u'aą':
            letters = concat_lists(letters, [u'a', u'ą'])
        elif letter in u'cč':
            letters = concat_lists(letters, [u'c', u'č'])
        elif letter in u'o':
            letters = concat_lists(letters, [u'o', u'uo'])
        elif letter in u'eęė':
            letters = concat_lists(letters, [u'e', u'ė', u'ę', u'ia'])
        elif letter in u'įiy':
            letters = concat_lists(letters, [u'į', u'i', u'y'])
        elif letter in u'šs':
            letters = concat_lists(letters, [u's', u'š'])
        elif letter in u'ųūu':
            letters = concat_lists(letters, [u'u', u'ų', u'ū'])
        elif letter in u'zž':
            letters = concat_lists(letters, [u'z', u'ž'])
        else:
            letters = concat_lists(letters, [letter])
    return letters



def known(words):
    return set(w for w in words if w in NWORDS)

# 1 stage leaves the word if it is known
# 2 stage edits letters by trying modifications with only lithuanian specific symbols without changing length of the word
# 3, 4 stages are all other kind of edits
def correct(word):
    if len(word) > 15:
        candidates = known([word]) or known(editsLTx(word)) or known(edits1(word)) or known_edits2(word) or set([word])
    else:
        candidates = known([word]) or known(editsLTx(word)) or known(editsLT(word)) or known(edits1(word)) or known_edits2(word) or set([word])
        # debug
        # print candidates
    if len(candidates) == 0:
        return word
    else:
        out = max(candidates, key=NWORDS.get)
        #if NWORDS[out] < 3:
        #    return u'\'' + word + u'\''
        #else:
        #    return out
        return out
