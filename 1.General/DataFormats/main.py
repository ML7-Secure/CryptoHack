from Crypto.PublicKey import RSA

def importKeyRSA(key_file):
    return RSA.importKey(open(key_file, 'r').read().rstrip('\n'))

def pem(keyPath):

    #keyPath = './DataFormats/privacy_enhanced_mail.pem'
    RSAkey = importKeyRSA(keyPath)
    print(RSAkey.n)
    print(RSAkey.p)
    print(RSAkey.q)
    print(RSAkey.d)

    # >>>>> openssl command : openssl rsa -text -in <privacy.pem> <<<<<
    # >>>>> openssl command : openssl asn1parse -inform PEM -in <transparency.pem> -strparse <offset> <<<<<


def der():
    # >>>>> openssl command : openssl asn1parse -inform DER -in <example.der> <<<<< !! NOT ENOUGH !!
    # >>>>> openssl command : openssl x509 -in <example-cert.der> -inform DER -text -noout <<<<<
    pass

def ssh(keyPath):
    #keyPath = './DataFormats/bruce_rsa.pub'
    RSAkey = importKeyRSA(keyPath)
    print(RSAkey.n)

    # >>>>> openssl command ? SSH here not directly RSA pubkey format ?  <<<<<
    
def main():
    #pem('./DataFormats/transparency.pem')
    #der()
    #ssh('./DataFormats/transparency.pem')
    
    # To get info on TLS certificates >>>>> https://crt.sh/ <<<<<
    pass

if __name__ == '__main__':
    main()