import hashlib
import sys
from socket import AF_INET, SOCK_STREAM, socket

bufsize = 1024

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind((sys.argv[1], int(sys.argv[2])))
    server.listen(1)
    client, _ = server.accept()

    with open(sys.argv[6], "wb") as fajl:
        checksum = hashlib.md5()
        while 1:
            data = client.recv(bufsize)
            if not data:
                break
            fajl.write(data)
            checksum.update(data)

    client.close()

print(checksum.hexdigest())

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect((sys.argv[3], int(sys.argv[4])))
    message = "KI|{}".format(int(sys.argv[5])).encode()
    client.sendall(message)
    reply = client.recv(bufsize)

checksum_len, checksum_rcv = reply.split(b"|")

print(checksum_rcv, checksum_len, checksum.hexdigest().encode())
if checksum_rcv and len(checksum_rcv) == int(checksum_len) and checksum_rcv == checksum.hexdigest().encode():
    print("CSUM OK")
else:
    print("CSUM CORRUPTED")