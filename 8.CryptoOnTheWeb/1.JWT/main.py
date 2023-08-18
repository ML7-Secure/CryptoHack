import jwt

import requests
def NoWayJOSE():#dinesh0x0d
    encoded = jwt.encode({'username': 'admin', 'admin': True}, None, algorithm='none')
    url =  'http://web.cryptohack.org/no-way-jose/authorise/'+encoded.decode()+'/'
    flag = requests.get(url)
    print(flag.text)

def JWTsecrets():#dinesh0x0d
    encoded = jwt.encode({'username':'admin', 'admin': True}, 'secret', algorithm='HS256')
    url = 'http://web.cryptohack.org/jwt-secrets/authorise/'+encoded.decode()+'/'
    flag =  requests.get(url)
    print(flag.text)

def jwt_decode(encoded):
    return jwt.decode(encoded, options={"verify_signature": False})

def main():
    encoded = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiY3J5cHRve2p3dF9jb250ZW50c19jYW5fYmVfZWFzaWx5X3ZpZXdlZH0iLCJ1c2VyIjoiQ3J5cHRvIE1jSGFjayIsImV4cCI6MjAwNTAzMzQ5M30.shKSmZfgGVvd2OSB2CGezzJ3N6WAULo3w9zCl_T47KQ"
    print( jwt_decode(encoded) )

    #NoWayJOSE()
    #JWTsecrets()

if __name__ == '__main__':
    main()