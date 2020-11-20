class Cache:
  def __init__(self):
    self.cache = {}
    self.cache_size = 20

  def get(self, vector):
    v = tuple(vector)
    if v in self.cache:
      return self.cache[v]
    return None
  
  def put(self, vector, result):
    v = tuple(vector)
    if len(self.cache) >= self.cache_size:
      self.cache.pop()
    self.cache[v] = result