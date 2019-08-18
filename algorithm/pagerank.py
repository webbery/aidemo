from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def likely_probability(vec_arr):
    n = vec_arr.shape[0]
    m = np.zeros((n, n))
    # i->j的相似程度,等价于pagerank中i页面到j页面的转化概率
    for i in range(n):
        for j in range(i + 1, n):
            m[i, j] = cosine_similarity(vec_arr[i].reshape(1, -1),
                                        vec_arr[j].reshape(1, -1))[0][0]
            m[j, i] = m[i, j]
    # for i in range(n):
    #     if not np.count_nonzero(m[i]):
    #         m[i] = np.full((1, n), 1 / n)
    print(m)
    return m
    # return preprocessing.normalize(m, norm='l1')

def PR_score(m,n=50):
    d = 0.85
    N = m.shape[0]
    # col = m.shape[1]
    PR=np.ones((N,1))
    out=np.zeros((N,1))
    for _ in range(n):
        for idx in range(N):
            sum_val = 0
            for i in range(N):
                if i!=idx:
                    sum_val += PR[i]*m[idx,i]
            PR[idx] = (1-d)/N+d*sum_val
    print(PR)
    return PR

# def score(m, mu=0.85, epsilon=0.0001, n=50):
#     score = np.full((m.shape[0], 1), 1)
#     for _ in range(n):
#         temp = score.copy()
#         score = mu * np.mat(m).T * score + (1 - mu) / m.shape[0]
#         print(score)
#         if max(abs(temp - score)) < epsilon:
#             break
#     print(score)
#     return score