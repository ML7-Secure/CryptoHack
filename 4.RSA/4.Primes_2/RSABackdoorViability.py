import logging
import os
import sys
from math import gcd

from sage.all import EllipticCurve
from sage.all import ZZ
from sage.all import Zmod
from sage.all import hilbert_class_polynomial
from sage.all import factor

# path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
# if sys.path[1] != path:
#     sys.path.insert(1, path)

# from shared.polynomial import polynomial_inverse
# from shared.polynomial import polynomial_xgcd

def polynomial_xgcd(a, b):
    """
    Computes the extended GCD of two polynomials using Euclid's algorithm.
    :param a: the first polynomial
    :param b: the second polynomial
    :return: a tuple containing r, s, and t
    """
    assert a.base_ring() == b.base_ring()

    r_prev, r = a, b
    s_prev, s = 1, 0
    t_prev, t = 0, 1

    while r:
        try:
            q = r_prev // r
            r_prev, r = r, r_prev - q * r
            s_prev, s = s, s_prev - q * s
            t_prev, t = t, t_prev - q * t
        except RuntimeError:
            raise ArithmeticError("r is not invertible", r)

    return r_prev, s_prev, t_prev


def polynomial_inverse(p, m):
    """
    Computes the inverse of a polynomial modulo a polynomial using the extended GCD.
    :param p: the polynomial
    :param m: the polynomial modulus
    :return: the inverse of p modulo m
    """
    g, s, t = polynomial_xgcd(p, m)
    return s * g.lc() ** -1


def factorize(N, D):
    """
    Recovers the prime factors from a modulus using Cheng's elliptic curve complex multiplication method.
    More information: Sedlacek V. et al., "I want to break square-free: The 4p - 1 factorization method and its RSA backdoor viability"
    :param N: the modulus
    :param D: the discriminant to use to generate the Hilbert polynomial
    :return: a tuple containing the prime factors
    """
    assert D % 8 == 3, "D should be square-free"

    zmodn = Zmod(N)
    pr = zmodn["x"]

    H = pr(hilbert_class_polynomial(-D))
    Q = pr.quotient(H)
    j = Q.gen()

    try:
        k = j * polynomial_inverse((1728 - j).lift(), H)
    except ArithmeticError as err:
        # If some polynomial was not invertible during XGCD calculation, we can factor n.
        p = gcd(int(err.args[1].lc()), N)
        return int(p), int(N // p)

    E = EllipticCurve(Q, [3 * k, 2 * k])
    while True:
        x = zmodn.random_element()

        logging.debug(f"Calculating division polynomial of Q{x}...")
        z = E.division_polynomial(N, x=Q(x))

        try:
            d, _, _ = polynomial_xgcd(z.lift(), H)
        except ArithmeticError as err:
            # If some polynomial was not invertible during XGCD calculation, we can factor n.
            p = gcd(int(err.args[1].lc()), N)
            return int(p), int(N // p)

        p = gcd(int(d), N)
        if 1 < p < N:
            return int(p), int(N // p)


sys.setrecursionlimit(20000)
# Paper w/ algo => https://www.scitepress.org/Papers/2019/77866/77866.pdf
D = 427
N = 709872443186761582125747585668724501268558458558798673014673483766300964836479167241315660053878650421761726639872089885502004902487471946410918420927682586362111137364814638033425428214041019139158018673749256694555341525164012369589067354955298579131735466795918522816127398340465761406719060284098094643289390016311668316687808837563589124091867773655044913003668590954899705366787080923717270827184222673706856184434629431186284270269532605221507485774898673802583974291853116198037970076073697225047098901414637433392658500670740996008799860530032515716031449787089371403485205810795880416920642186451022374989891611943906891139047764042051071647203057520104267427832746020858026150611650447823314079076243582616371718150121483335889885277291312834083234087660399534665835291621232056473843224515909023120834377664505788329527517932160909013410933312572810208043849529655209420055180680775718614088521014772491776654380478948591063486615023605584483338460667397264724871221133652955371027085804223956104532604113969119716485142424996255737376464834315527822566017923598626634438066724763559943441023574575168924010274261376863202598353430010875182947485101076308406061724505065886990350185188453776162319552566614214624361251463
print( factorize(N, D) )

