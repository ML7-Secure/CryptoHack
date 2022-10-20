import numpy as np


def dotProduct(u,v):
    n = len(v)
    res = 0
    for i in range(n):
        res += u[i]*v[i]

    return res


"""
V : List of vectors
"""
# V = [v1, v2, v3, v4]

def SemiGramSchmidt(v): # GS w/o orthonormalization
    u = [v[0]]
    for vi in v[1:]:
        mi = [np.dot(vi, uj) / np.dot(uj, uj) for uj in u]
        u += [vi - sum([mij * uj for (mij, uj) in zip(mi,u)])]

    return u

    # SAGE SOLUCE 
    """ 
    v0 = vector([4,1,3,-1])
    v1 = vector([2,1,-3,4])
    v2 = vector([1,0,-2,7])
    v3 = vector([6,2,9,-5])
    M = Matrix([v0,v1,v2,v3])
    M.gram_schmidt()
    """

def siz2(v):
    return np.dot(v, v)
    

def gaussianReduction(u,v): # 2-dim case w/ Numpy => https://programming.vip/docs/cryptohack-title-record-mathematics-section-lattice-writeup.html
    v1,v2 = u,v
    m = 1
    while m != 0:
        if siz2(v2) < siz2(v1):
            print('swap')
            v1,v2 = v2,v1
        
        m = int(v1.dot(v2)/v1.dot(v1)) # pivot ?
        v2 = v2 - m*v1
    
    return v1,v2

def main():
    # v1 = np.array([4,1,3,-1]); v2 = np.array([2,1,-3,4])
    # v3 = np.array([1,0,-2,7]); v4 = np.array([6, 2, 9, -5]) 
    # v = [v1,v2,v3,v4]
    # res = SemiGramSchmidt(v)
    # print(round(res[3][1], 5))

    # print(dotProduct([4,6,2,5], [4,6,2,5]))

    # ar = np.array
    # v = ar([846835985, 9834798552],dtype='i8')
    # u = ar([87502093, 123094980],dtype='i8')
    # res = gaussianReduction(u,v)
    # print(np.dot(res[0],res[1]))
    
    
    def Gauss(v1, v2): # w/ Sage
        while True:
            if v2.norm() < v1.norm():
                v1, v2 = v2, v1
            m = round( v1*v2 / v1.norm()^2 )
            if m == 0:
                return (v1, v2)
            v2 = v2 - m*v1
    
    # Look at source1.py
    """
    PublicKey = [7638232120454925879231554234011842347641017888219021175304217358715878636183252433454896490677496516149889316745664606749499241420160898019203925115292257, 2163268902194560093843693572170199707501787797497998463462129592239973581462651622978282637513865274199374452805292639586264791317439029535926401109074800]
    EncFlag = 5605696495253720664142881956908624307570671858477482119657436163663663844731169035682344974286379049123733356009125671924280312532755241162267269123486523
    h = PublicKey[1]
    q = PublicKey[0]

    v = vector([1,h])
    u = vector([0,q])
    Gauss(u, v)
    """

    # Look at source2.py
    


if __name__ == '__main__':
    main()
    