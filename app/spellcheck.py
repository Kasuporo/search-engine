import re, collections

alphabet = 'abcdefghijklmnopqrstuvwxyz'
NWORDS = ''
class check:
    
    def __init__(self, word):
        self.word = word

    def words(self, text):
        return re.findall('[a-z]+', text.lower())

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self, word):
        global alphabet
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in s if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
        inserts    = [a + c + b     for a, b in s for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        global NWORDS
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if\
                                                                  e2 in NWORDS)

    def known(self, words):
        return set(w for w in words if w in NWORDS)

    def correct(self, word):
        global NWORDS
        NWORDS = self.train(self.words(open('app/big.txt').read()))
        candidates = self.known([self.word]) or self.known(self.edits1(word))\
                                or self.known_edits2(self.word) or [self.word]
        return max(candidates, key=NWORDS.get)
