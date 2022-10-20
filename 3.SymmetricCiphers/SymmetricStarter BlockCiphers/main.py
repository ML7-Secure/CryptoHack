
import requests
def get(request):
    base_url="http://aes.cryptohack.org/"
    req = requests.get(base_url+request)
    return req.json()

def decryptAPI(ciphertext, page:str):
    dico = get(page+'decrypt/'+ciphertext)
    plaintext = dico['plaintext']
    plain = int(plaintext,16) # To int
    p = plain.to_bytes(len(plaintext)//2, 'big')
    return p
    #return p.decode() 

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
    print(ct)
    
if __name__ == '__main__':
	main()