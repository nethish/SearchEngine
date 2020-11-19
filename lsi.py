import numpy as np

def lsi_matrix(matrix, K=5):
  U, s, VT = np.linalg.svd(matrix)
  reduced_matrix = np.dot(U[:, :K], np.dot(np.diag(s[:K]), VT[:K, :]))
  return reduced_matrix
