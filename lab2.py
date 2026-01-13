import numpy as np
import time


def fast_matrix_multiply(A, B):
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        CC=C[i]
        AA=A[i]
        for k in range(n):
            BB=B[k]
            a_ik = AA[k]
            for j in range(n):
                CC[j] += a_ik * BB[j]
    return C


n = 512
np.random.seed(42)
A = np.random.rand(n, n).tolist()
B = np.random.rand(n, n).tolist()

start = time.time()
C = fast_matrix_multiply(A, B)
elapsed = time.time() - startstart = time.time()
C = A * B
elapsed = time.time() - start
print(f"умножение ({n}x{n}): за {elapsed:.2f} с")
print(f"умножение ({n}x{n}): за {elapsed:.2f} с")

