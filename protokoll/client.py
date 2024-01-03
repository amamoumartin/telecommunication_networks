import struct,sys
res,formats,newFormats,values = [], ['f ? c', 'c 9s i', 'i ? f', 'c f 9s'],['11s i ?','f ? c', 'i 9s f', 'c i 12s'],[('elso'.encode(),51,True), (54.5,False,'X'.encode()),(42,'masodik'.encode(),61.9),('Z'.encode(),73,'harmadik'.encode())]
for i,arg in enumerate((sys.argv)[1::]):
    with open(arg,'rb') as f:
        res.append(struct.unpack(formats[i],f.read(struct.calcsize(formats[i]))))
for i in range(4):
    res.append(struct.Struct(newFormats[i]).pack(*values[i]))
for i in range(len(res)):print(res[i])