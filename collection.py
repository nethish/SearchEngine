import pickle
from collections import defaultdict
from scrape import get_tokens, get_text
from math import log

def getDD():
    return defaultdict(int)

class Collection:
    def __init__(self):
        self.urls = {}
        self.corpus = set()
        self.postings = defaultdict(getDD)
        self.tdf = defaultdict(getDD)
        self.terms = dict()
        self.vocabulary = 0
        self.size = 0

    def add_document(self, url):
        if url in self.urls:
            return
        tokens = get_tokens(url)
        if len(tokens) == 0:
            return
        DOC_ID = len(self.urls) + 1
        self.urls[DOC_ID] = url
        self.corpus.add(url)
        self.size += 1
        for tok in tokens:
            if tok not in self.terms:
                self.vocabulary += 1
                self.terms[tok] = self.vocabulary
            self.tdf[DOC_ID][tok] += 1
            doc_list = self.postings[tok]
            doc_list[DOC_ID] += 1
            self.postings[tok] = doc_list

    def get_tdf(self, doc, term):
        return self.tdf[doc][term]

    def get_dft(self, term):
        return len(self.postings[term])

    def get_tfidf(self, doc, term):
        tdf = self.get_tdf(doc, term)
        dft = self.get_dft(term)
        return (log(tdf + 2)) * log(self.size / (1 +dft))

    def get_url(self, id):
        return self.urls[id]

    # def get_postings(self):
    #     for i in self.postings:
    #         print('Word:', i)
    #         for j in self.postings[i]:
    #             print('Doc: %d, Freq: %d'%(j, self.postings[i][j]), end = ' | ')
    #         print('\n------------------------------')
    #     print()
    #     return self.postings

if __name__ == "__main__":
    links = open("./Links.txt", 'r').read().split('\n')
    collection = Collection()
    for link in links:
        collection.add_document(link)
    collection.get_postings()
