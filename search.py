from collection import Collection
import re, os
import pickle
from math import log

class Search:
  def __init__(self, collection):
    self.collection = collection
    self.terms = []
    self.search_limit = 5
    self.set_collection(collection)

  def set_collection(self, collection):
    self.collection = collection
    self.terms = []
    for term in self.collection.terms:
      self.terms.append(term)

  def get_collection(self):
    return self.collection

  def cosine(self, a, b):
    n = len(a)
    dot = 0
    norm_a = norm_b = 0
    for i in range(n):
      dot += a[i] * b[i]
      norm_a += a[i] ** 2
      norm_b += b[i] ** 2
    if not norm_a or not norm_b:
      return 0
    cos = dot / (norm_a * norm_b) ** 0.5
    return cos

  def structure_query(self, query):
    terms = re.split('\W+', query)
    for i in range(len(terms)):
      terms[i] = terms[i].lower()
    query = []
    for t in self.terms:
      cnt = terms.count(t)
      if not cnt:
        query.append(0)
        continue
      query.append(log(log(cnt + 2)) * log((self.collection.size + 1) / (2 + self.collection.get_dft(t))))
    return query

  def search(self, query):
    # result = []
    # terms = re.split('\W+', query)
    # query = []
    # for t in self.terms:
    #   cnt = terms.count(t)
    #   if not cnt:
    #     query.append(0)
    #     continue
    #   query.append(log(1 + log(cnt)) * log((self.collection.size + 1) / (1 + self.collection.get_dft(t))))
    query = self.structure_query(query)

    if not query:
      return ["No match found"]
    
    result = []
    for doc in range(1, len(self.collection.urls) + 1):
      doc_vector = self.construct_doc(doc)
      # for t in self.terms:
      #   doc_vector.append(self.collection.get_tfidf(doc, t)) #self.collection.tdf[doc][t])
      result.append((self.cosine(doc_vector, query), doc))
    
    result.sort()
    search_results = []
    for i in range(min(self.search_limit, len(result))):
      search_results.append(self.collection.get_url(result[i][1]))
    # print(result)
    return search_results

  def construct_doc(self, doc):
    doc_vector = []
    for t in self.terms:
      doc_vector.append(self.collection.get_tfidf(doc, t))
    return doc_vector

  def update_collection(self, links):
    for link in links:
      if link not in self.collection.corpus:
        print("Updated: ", self.collection.size)
        self.collection.add_document(link)
    self.set_collection(self.collection)
    collection_loader = CollectionLoader()
    collection_loader.dump(self.collection)

class CollectionLoader:
  def __init__(self):
    pass

  def dump(self, collection, file='index.pickle'):
    with open(file, 'wb') as handle:
      pickle.dump(collection, handle)

  def load(self, file='index.pickle'):
    file = open('index.pickle', 'rb')
    collection = pickle.load(file)
    file.close()
    return collection

if __name__ == "__main__":
    links = open("./Links.txt", 'r').read().split('\n')
    collection_loader = CollectionLoader()
    if os.path.isfile('index.pickle'):
      print('Loading...')
      collection = collection_loader.load()
    else:
      print('Scraping...')
      collection = Collection()
      collection_loader.dump(collection)
    search = Search(collection)
    search.update_collection(links)
    # print(collection.terms)
    query = input('>>> Search: ')
    while query != 'exit':
      result = search.search(query)
      for i in result:
        print(i)
      query = input('>>> Search: ')
