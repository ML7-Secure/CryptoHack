from Crypto.Util.number import bytes_to_long, long_to_bytes
import functools
import operator

import requests

def get(request):
    base_url="http://aes.cryptohack.org/"
    req = requests.get(base_url+request)
    return req.json()

def decryptAPI(ciphertext, page:str):
    dico = get(page+'decrypt/'+ciphertext)
    plaintext = dico['plaintext']
    return plaintext
    """
    plain = int(plaintext,16) # To int
    p = plain.to_bytes(len(plaintext)//2, 'big')
    try:
        print(p.decode())
    except UnicodeDecodeError as e:
        print(e)
    return p
    """

def encryptFlagAPI(page:str):
    dico = get(page+'encrypt_flag/')
    return dico

from Crypto.Cipher import AES
import hashlib
def passwordsAsKeys(ct, page):

    with open("/usr/share/wordlists/words") as f:
        words = [w.strip() for w in f.readlines()]
    
    for word in words:
        print(word)
        key = hashlib.md5(word.encode()).hexdigest()
        ciphertext = ct+'/'+key+'/'
        flag = decryptAPI(ciphertext, page)
        try:
            res = flag.decode()
            print(res)
            return
        except UnicodeDecodeError:
            continue

def main():
    ## AES Modes ##
    # c = "b85276b96d227791da064c35830653f558c61e68ac802b659dcf619a123f8f1b"
    # page = 'block_cipher_starter/'
    # print(decryptAPI(c, page))

    # page = "passwords_as_keys/"
    # dico = encryptFlagAPI(page)
    # ct = dico['ciphertext']
    # passwordsAsKeys(ct, page)
    
    page = "ecbcbcwtf/"
    dico = encryptFlagAPI(page)
    ct = dico['ciphertext']

    iv = ct[0:32]
    cipher = ct[32:]
    plain = decryptAPI(ct[32:], page)

    res = int(plain[0:32],16) ^ int(iv, 16) # 1st block
    flag1 = long_to_bytes(res)
    
    res = int(plain[32:],16) ^ int(cipher[:32], 16) # 2nd block
    flag2 = long_to_bytes(res)

    flag = flag1+flag2
    print(flag)


if __name__ == '__main__':
	main()