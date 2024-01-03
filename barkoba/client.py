import socket,sys,struct,math,time

hostname,port = sys.argv[1],int(sys.argv[2])
packer = struct.Struct("1s I")
rel = '<'
alsoErtek,felsoErtek = 1,100
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostname,port))
on = True

def kozep(a,b):
    return math.floor((a+b)/2)

def tipp(also,felso,rel):
    if(also == felso):
        print("tipp:=" + " " + str(also))
        data = packer.pack("=".encode(),also)
        client.send(data)
    else:
        num = kozep(also,felso)
        print("tipp:" + rel + " " + str(num))
        data = packer.pack(rel.encode(),num)
        client.send(data)

def fogad(alsoErtek,felsoErtek):
    d = client.recv(packer.size)
    valasz,_ = packer.unpack(d)
    valasz = valasz.decode()
    print("szerver szerint:" + valasz)
    if(valasz == 'Y' or valasz == 'V' or valasz == 'K'):
        return 0,0,True
    if(rel == '>'):
        if(valasz == 'N'):
            felsoErtek = kozep(alsoErtek,felsoErtek)
        else:
            alsoErtek = kozep(alsoErtek,felsoErtek) + 1
    elif(rel == '<'):
        if(valasz == 'I'):
            felsoErtek = kozep(alsoErtek,felsoErtek) - 1
        else:
            alsoErtek = kozep(alsoErtek,felsoErtek)
    return alsoErtek, felsoErtek,False


while on:
    time.sleep(1)
    tipp(alsoErtek,felsoErtek,rel)
    alsoErtek,felsoErtek,vege = fogad(alsoErtek,felsoErtek)
    if(vege):
        on = False
    if(rel == '<'):
        rel = '>'
    else:
        rel = '<'