"""
Returns gcd(a,b)
"""
def my_gcd(a, b): 
    while(b != 0):
        a, b = b, a % b
    return a

"""
extended gcd
"""
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def euclide_etendu(a, b):
    x,y, u,v = 0,1, 1,0 
    while a != 0: 
        q, r = b//a, b%a 
        m, n = x-u*q, y-v*q 
        b,a, x,y, u,v = a,r, u,v, m,n 
    return b,x#,y
    # b == gcd
    # x == coeff 'u'
    # y == coeff 'v'

a=26513
b=32321
# print(my_gcd(a, b))
# print(egcd(a, b))
#print(euclide_etendu(a, b))



def my_inverse(a, N):
    g, x = euclide_etendu(a, N)
    if g != 1: 
        return None # a is not inversible mod N
    else: 
        return x % N

print(my_inverse(3, 13))