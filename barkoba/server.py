import socket,sys,random,struct,select,time

solution = random.randrange(100) + 1
hostname,port = sys.argv[1],int(sys.argv[2])
def check(op,number):
    if op == '<':
        return ('I' if solution < number else 'N')
    elif op == '>':
        return ('I' if solution > number else 'N')
    elif op == '=':
        return ('Y' if solution == number else 'K')

packer = struct.Struct("1s I")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((hostname,port))
	server.listen(10)

	inputs,clients = [server],[]

	while True:
		try:
			r,_,_ = select.select(inputs,[],[])
			for s in r:
				if s is server:
					client,client_addr = server.accept()
					print("uj kliens: " + str(client_addr))
					clients.append(client)
					inputs.append(client)
				else:
					data = s.recv(packer.size)
					if data:
						op,number = packer.unpack(data)
						result = check(op.decode(),number)
						s.send(packer.pack(result.encode(),0))
						if(result == "Y"):
							inputs.remove(s)
							clients.remove(s)
							for cl in clients:
								cl.send(packer.pack(b'V',0))
								inputs.remove(cl)
								clients.remove(cl)
							time.sleep(1)
							solution = random.randrange(100) + 1
							print("uj szam:" + str(solution))
		except Exception:
			for cl in clients:
				cl.close()
			server.close()