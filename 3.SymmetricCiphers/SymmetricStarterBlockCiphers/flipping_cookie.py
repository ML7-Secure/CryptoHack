from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
import requests


def get(request):
    base_url="http://aes.cryptohack.org/"
    req = requests.get(base_url+request)
    return req.json()

def check_admin(cookie, iv):
    page = "/flipping_cookie/check_admin/"+cookie+"/"+iv+"/"
    dico = get(page)
    return dico

def get_cookie():
    page = "/flipping_cookie/get_cookie/"
    dico = get(page)
    return dico

def flip(cookie, original_plain):
    # original_plain = b"admin=False;expiry={expires_at}"

    cookie = bytes.fromhex(cookie)

    goal_iv = [0]*16 # IV to be forged
    goal_cipher = list(cookie) # Cipher to be forged
    goal_plain = b";admin=True;" # Plain to be forged (to be read by target server)

    for i in range(len(goal_plain)):
        goal_cipher[16+i] = original_plain[16+i] ^ cookie[16+i] ^ goal_plain[i] # C' = P1 ^ C ^ P1'
        goal_iv[i] = original_plain[i] ^ cookie[i] ^ goal_plain[i]              # IV' = P ^ IV ^ P'
        #                                ^^^^^^^^
        #                                   IV

    goal_cipher = bytes(goal_cipher).hex()
    goal_iv = bytes(goal_iv).hex()

    return goal_cipher, goal_iv

def main():
    expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    original_plain = f"admin=False;expiry={expires_at}".encode()

    dico = get_cookie()
    cookie = dico['cookie']

    goal_cipher, goal_iv = flip(cookie, original_plain)

    check_admin(goal_cipher, goal_iv)
    res = check_admin(goal_cipher, goal_iv)
    print(res)

#main()

# Better (more clear) solution : https://blog.csdn.net/shshss64/article/details/128080636 
from Crypto.Util.number import *
def another_solution():
    dico = get_cookie()
    m = dico['cookie']

    IV = m[:32]
    k = m[32:] # cookie

    a1 = b'admin=False;expi' # original plain - SIZE ARE IMPORTANT !
    a2 = b'admin=True;00000' # goal plain - SIZE ARE IMPORTANT !

    m1 = hex(bytes_to_long(a1))[2:]
    m2 = hex(bytes_to_long(a2))[2:]

    IV_new = int(m1,16) ^ int(m2,16) ^ int(IV,16) # goal IV (forged) ==  P_orig ^ P_goal ^ IV_orig
    IV_new = hex(IV_new)[2:]

    res = check_admin(k, IV_new)
    print(res['flag'])

another_solution()

"""
P = C ^ IV
C = P ^ IV (*)

=> P_goal = C ^ IV_goal 
=> IV_goal = C ^ P_goal 
(*) => IV_goal = P ^ IV ^ P_goal
               = P_orig ^ IV_orig ^ P_goal 
"""