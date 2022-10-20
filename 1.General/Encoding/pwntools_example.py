from pwn import * # pip install pwntools
import json

import codecs
from Crypto.Util.number import bytes_to_long, long_to_bytes

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


received = json_recv()

print("Received type: ")
receivedType = received["type"] 
print(receivedType)

print("Received encoded value: ")
receivedValue = received["encoded"]
print(receivedValue)

if receivedType == "base64":
    decoded = base64.b64decode(receivedValue).decode() # wow so encode

elif receivedType == "hex":
    decoded = bytes.fromhex(receivedValue)

elif receivedType == "rot13":
    decoded = codecs.decode(receivedValue, 'rot_13')

elif receivedType == "bigint":
    decoded = hex(long_to_bytes(receivedValue))

elif receivedType == "utf-8":
    decoded = [chr(b) for b in receivedValue]


to_send = {
    "decoded": decoded
}
json_send(to_send)

json_recv()
