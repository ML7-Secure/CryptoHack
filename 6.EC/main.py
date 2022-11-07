from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes#, isPrime, GCD
from hashlib import sha1

def f(x, y, a, b, p):
    return ( pow(x, 3, p) + a * x + b - pow(y, 2, p) ) % p

def pointAddition(Px, Py, Qx, Qy, a, mod):
    if Px == 0 and Py == 0:
        return Qx, Qy

    elif Qx == 0 and Qy == 0:
        return Px, Py

    elif Px == Qx and Py == -Qy:
        return (0, 0)

    else:
        if Px != Qx and Py != Qy:
            lmbda = ( (Qy - Py) * inverse(Qx - Px, mod) ) % mod

        elif Px == Qx and Py == Qy:
            lmbda = ( (3*pow(Px, 2, mod) + a) * inverse(2*Py, mod) ) % mod

        else:
            print('Not supported operation')
    
    x3 = ( pow(lmbda, 2, mod) - Px - Qx ) % mod
    y3 = ( lmbda*(Px - x3) - Py ) % mod
    S = (x3, y3)
    return S

def scalarMultiplication(Px, Py, n, a, mod):
    Qx = Px
    Qy = Py
    Rx = Ry = 0
    while n > 0:
        if (n % 2) == 1 :
            R = pointAddition(Rx, Ry, Qx, Qy, a, mod)
            Rx = R[0]
            Ry = R[1]

        Q = pointAddition(Qx, Qy, Qx, Qy, a, mod)
        Qx = Q[0]
        Qy = Q[1]
        n //= 2
    return R

def EC_keyExchange(Qa, nB, a, mod):
    # Bob's side :
    # Qa = nA * G
    Qa_x = Qa[0]
    Qa_y = Qa[1]
    S = scalarMultiplication(Qa_x, Qa_y, nB, a, mod)
    S_x = S[0]
    key = sha1(str(S_x).encode()).hexdigest()
    return key

    # Alice's side :
    # Qb = nB * G 
    # Qb_x = Qb[0]
    # Qb_y = Qb[1]
    # assert S == scalarMultiplication(Qb_x, Qb_y, nA, a, mod)

def efficient_EC_keyExchange(Qa_x, nB, a, mod):
    # Use curve to find 'y'
    S = scalarMultiplication(Qa_x, Qa_x, nB, a, mod)
    S_x = S[0]
    return S_x

def main():
    # Px = 5274
    # Py = 2841
    # Qx = 8669
    # Qy = 740
    mod = 9739
    a = 497
    #print( pointAddition(Px, Py, Qx, Qy, a, mod) )

    # Px = 493
    # Py = 5564
    # Qx = 1539
    # Qy = 4742
    # Rx = 4403
    # Ry = 5202
    
    # PplusP = pointAddition(Px, Py, Px, Py, a, mod)
    # QplusR = pointAddition(Qx, Qy, Rx, Ry, a, mod)
    # x1 = PplusP[0]
    # y1 = PplusP[1]
    # x2 = QplusR[0]
    # y2 = QplusR[1]
    # S = pointAddition(x1, y1, x2, y2, a, mod)
    # print(S)
    # x = S[0]
    # y = S[1]
    b = 1768

    #Px = 5323
    #Py = 5438
    #n = 1337

    # Px = 2339
    # Py = 2213
    # n = 7863

    # Q = scalarMultiplication(Px, Py, n, a, mod)
    # print(Q)
    # x = Q[0]
    # y = Q[1]
    
    #print( f(x, y, a, b, mod) )

    # Qa = (815, 3190)
    # nB = 1829
    # key = EC_keyExchange(Qa, nB, a, mod)
    # print(key)

    Qa_x = 4726
    nB = 6534
    S = efficient_EC_keyExchange(Qa_x, nB, a, mod)
    print(S)
    
if __name__ == '__main__':
    main()