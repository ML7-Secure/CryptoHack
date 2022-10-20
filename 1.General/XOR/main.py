
import functools
import operator

def XOR(*seqs):
    return bytearray([functools.reduce(operator.xor, t, 0) for t in zip(*seqs)])

"""
s : bytes
toXor : int
"""
def starter(s, toXor):

    c = []
    for char in s:
        c.append(char ^ toXor)

    res=''
    for i in c:
        res += chr(i)

    return res


def properties():

    key1 = 0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
    key1 = key1.to_bytes(26, 'big')
    
    hex1 = 0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
    hex1 = hex1.to_bytes(26, 'big')

    key2 = XOR(key1, hex1)

    hex2 = 0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
    hex2 = hex2.to_bytes(26, 'big')

    key3 = XOR(key2, hex2)
    
    hex3 = 0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
    hex3 = hex3.to_bytes(26, 'big')
    
    flag = XOR(key1, key2, key3, hex3)
    return flag.decode()


def favByte():
    h = 0x73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d

    length = (len(hex(h)) - 2) // 2
    h = h.to_bytes(length, 'big')

    for i in range(256):
        tmp = starter(h, i)
        if 'crypto' in tmp:
            print(tmp)


"""
h : string hex number w/o '0x'
"""
def hex2bytes(h):
    return bytes.fromhex(h)

def otp():
    c_hex = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
    c = hex2bytes(c_hex)

    plain = b"crypto{"
    #print(plain.hex())
    last = b'}'
    #print(last.hex())
    
    #print(XOR(plain, hex2bytes(c_hex[:14]))) # K = "myXORke..."
    #print(XOR(last, hex2bytes(c_hex[-2:]))) # K = "...y"

    K = b"myXORkey"
    K = b"myXORkey"*(len(c_hex) // len(K))
    print(XOR(c, K))

def lemur():
    with open('./XOR/lemur.png', 'rb') as img1:
        i1 = img1.read()

    with open('./XOR/flag.png', 'rb') as img2:
        i2 = img2.read()

    maskOff = XOR(i1,i2)
    #flag = XOR(maskOff, i1)
    
    with open('./XOR/res.png', 'wb') as res:
        #res.write(flag)
        res.write(maskOff)
    
    # WRONG : https://crypto.stackexchange.com/questions/88430/how-to-decrypt-two-images-encrypted-using-xor-with-the-same-key

def lemurSoluce():
    import numpy as np
    from PIL import Image

    img1 = Image.open('./XOR/lemur.png')
    img2 = Image.open('./XOR/flag.png')

    n1 = np.array(img1)*255
    n2 = np.array(img2)*255

    #our images have a mode of RGB which is assumed to be an 8-bit int
    n_image = np.bitwise_xor(n1, n2).astype(np.uint8)
    #Convert to PIL image and save
    Image.fromarray(n_image).save('./XOR/res.png')

def main():
    #print(starter(b'label', 13))
    #print(properties())
    #favByte()
    #otp()
    lemurSoluce()

if __name__ == '__main__':
    main()