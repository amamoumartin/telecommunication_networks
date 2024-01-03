import socket,select,sys,time
from bisect import insort
from itertools import dropwhile, takewhile

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((sys.argv[1], int(sys.argv[2])))
sock.listen(1)
input,exptimes,checksums = [sock],[],{}

while 1:
    try:
        read, _, _ = select.select(input, [], [])

        for s in read:
            if s is sock:
                connection, _ = sock.accept()
                input.append(connection)
            else:
                message = s.recv(1024)

                if not message:
                    s.close()
                    input.remove(s)
                    continue

                intent, fileid, *param = message.split(b"|")
                fileid = int(fileid)

                if intent == b"BE":
                    ttl, checksum_len, checksum = param
                    exp_time = time.time() + int(ttl)

                    if fileid in checksums:
                        exptimes.remove((checksums[fileid][0], fileid))

                    insort(exptimes, (exp_time, fileid))
                    checksums[fileid] = (exp_time, checksum_len, checksum)

                    if int(checksum_len) != len(checksum):
                        print(f"Unexpected checksum: {checksum} with length {checksum_len}")

                    reply = b"OK"
                elif intent == b"KI":
                    if fileid in checksums:
                        reply = b"|".join(checksums.pop(fileid)[1:])
                    else:
                        reply = b"0|"
                else:
                    print("Unexpected intent: " + intent + '(message: ' + message +")")

                s.sendall(reply)

                for _, fileid in takewhile(lambda t: t[0] < time.time(), exptimes):
                    checksums.pop(fileid)

                exptimes = list(dropwhile(lambda t: t[0] < time.time(), exptimes))
    except Exception:
        for i in input:
            i.close()
        break