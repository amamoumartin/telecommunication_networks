import hashlib,sys
from socket import AF_INET, SOCK_STREAM, socket

bufsize = 1024
with socket(AF_INET, SOCK_STREAM) as client:
    client.connect((sys.argv[1], int(sys.argv[2])))
    with open(sys.argv[6], "rb") as f:
        checksum = hashlib.md5()
        while 1:
            data = f.read(bufsize)
            if not data:
                break
            client.sendall(data)
            checksum.update(data)

    checksumbyte = checksum.hexdigest().encode()
    message = "BE|{}|{}|{}|{}".format(int(sys.argv[5]), 60, len(checksumbyte), checksumbyte).encode()
    print(message)


with socket(AF_INET, SOCK_STREAM) as client:
    client.connect((sys.argv[3], int(sys.argv[4])))
    client.sendall(message)
    answer = client.recv(bufsize)

    if answer != b"OK":
        print("Hiba,kapott valasz: " + answer)