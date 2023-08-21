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

def encryptAPI(page:str, plain:str):
    dico = get(page+'encrypt/'+plain)
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

def ecbOracle():
    #crypto{flagflagflagflagflagflagz}
    page = "ecb_oracle/"
    
    #plain = "AA"*7
    plain = 'AA' * 7 + 'AA' * 16 # For the 9 last chars to find ----
    
    pad_count = 0xf

    blank_block = 'c0ab7314c00f986d20da2942f2af75d3' # Needed when block size (16) is exceeded

    #flag_hex = ''
    flag_hex = '6e3675316e355f683437335f3363627d' # For the 9 last chars to find ----
    while len(flag_hex) < 32 + 18 : # For the 9 last chars to find ---- 18 = 9 bytes
    #while len(flag_hex) < 32: 
        plain = plain + "AA" # Add one byte to send the targeted byte to the padding block (=)
        dico = encryptAPI(page, plain)
        ct = dico['ciphertext']
        #last_block = ct[-32:]
        last_block = ct[-64:-32] # For the 9 last chars to find ---- Last block is now our current guess
        if last_block == blank_block:
            last_block = ct[-64:-32] # if there were more chars this would have to be edit to consider the new last block (=> ct[-96:-64])
            pad_count = 0xf + 1 # when block size (16) is exceeded pad is reinit to 16 
 
        for i in range(0x21, 0x7f): # ASCII VALUES ONLY (time is precious)
            testedByte = hex(i)[2:].zfill(2)
            #print("Testing... :", testedByte)
            inputPlain = testedByte + flag_hex + hex(pad_count)[2:].zfill(2) * pad_count # Add flag_hex to have the correct padding block length (=)
            #print("Testing... :", inputPlain)
            dico = encryptAPI(page, inputPlain)
            ct = dico['ciphertext']
            first_block = ct[:32]
            if first_block == last_block:
                print("OK :", testedByte)
                flag_hex = testedByte + flag_hex # IMPORTANT FOR THE ORDER (attack from the end)
                break
        pad_count -= 1 # plain = testedByte + "0e" * 0xe then plain = testedByte + "0d" * 0xd then ...
        print("current guess : ", flag_hex)

    flag = int(flag_hex[:18], 16).to_bytes(9).decode() # For the 9 last chars to find ----
    #flag = int(flag_hex, 16).to_bytes(16).decode()
    print(flag) # crypto{p3 # The 9 last chars to find ----
    #print(flag) # n6u1n5_h473_3cb}

def main():
    ## AES Modes ##
    # c = "b85276b96d227791da064c35830653f558c61e68ac802b659dcf619a123f8f1b"
    # page = 'block_cipher_starter/'
    # print(decryptAPI(c, page))

    # page = "passwords_as_keys/"
    # dico = encryptFlagAPI(page)
    # ct = dico['ciphertext']
    # passwordsAsKeys(ct, page)
    
    # page = "ecbcbcwtf/"
    # dico = encryptFlagAPI(page)
    # ct = dico['ciphertext']

    # iv = ct[0:32]
    # cipher = ct[32:]
    # plain = decryptAPI(ct[32:], page)

    # res = int(plain[0:32],16) ^ int(iv, 16) # 1st block
    # flag1 = long_to_bytes(res)
    
    # res = int(plain[32:],16) ^ int(cipher[:32], 16) # 2nd block
    # flag2 = long_to_bytes(res)

    # flag = flag1+flag2
    # print(flag)

    ecbOracle()


if __name__ == '__main__':
	main()