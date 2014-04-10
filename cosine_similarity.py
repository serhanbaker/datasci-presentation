import math

def cosine_similarity(v1,v2):
    """
    computes cosine similarity of v1 to v2: (v1 dot v1)/{||v1||*||v2||)
    """
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

#cosine_similarity([1,2,3,4,5], [4, 4.25, 4.50, 4.75, 5])