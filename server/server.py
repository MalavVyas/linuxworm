import socket, select, sys, os, time

#Function to send message to all connected clients
def send_to_all (message, connected_list):
	#Message not forwarded to server and sender itself
	for i in range(1, connected_list.__len__()):
		socket = connected_list[i]
		if socket != server_socket:
			socket.send(str(message).encode('utf-8'))
			# try :
			# except :
			# 	print("error in sending message")
				# if connection not available
				# socket.close()
				# connected_list.remove(socket)

"""
Sends script file to all clients
"""
def send_file(filename, connected_list):
	print("sending file")
	filesize = os.path.getsize(filename)
	print(filesize)
	for i in range(1, connected_list.__len__()):
		socket = connected_list[i]
		if socket != server_socket:
			SEPARATOR = "<SEPARATOR>"
			socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
			time.sleep(1)
			with open(filename, "rb") as f:
				it = 0
				while filesize > it:
					# read the bytes from the file
					bytes_read = f.read(4096)
					if not bytes_read:
						# file transmitting is done
						break
					# we use sendall to assure transimission in 
					# busy networks
					socket.sendall(bytes_read)

					it += 4096

if __name__ == "__main__":
	name=""
	banner = str.encode("Welcome to chat room. Enter 'tata' anytime to exit\n")
	#dictionary to store address corresponding to username
	record={}
	# List to keep track of socket descriptors
	connected_list = [sys.stdin]
	buffer = 4096
	port = 5001

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("localhost", port))
	server_socket.listen(10) #listen atmost 10 connection at one time

	# Add server socket to the list of readable connections
	connected_list.append(server_socket)

	print("SERVER WORKING")

	while 1:
		# Get the list sockets which are ready to be read through select
		rList,wList,error_sockets = select.select(connected_list,[],[])

		for sock in rList:
			#New connection
			if sock == server_socket:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()
				name=sockfd.recv(buffer)
				connected_list.append(sockfd)
				record[addr]=""
				#print "record and conn list ",record,connected_list

				#if repeated username
				if name in record.values():
					sockfd.send(b"Username already taken!")
					del record[addr]
					connected_list.remove(sockfd)
					sockfd.close()
					continue
				else:
					#add name and address
					record[addr]=name
					print("Client (%s, %s) connected" % addr," [",record[addr],"]")
					sockfd.send(banner)
					print(str(name) + "Joined")
					# send_to_all(sockfd, "\33[32m\33[1m\r "+str(name)+" joined the conversation \n\33[0m")

			#TODO: THIS IS WHERE DATA IS SENT
			#Some incoming message from a client
			elif sock == sys.stdin:
				input = str(sys.stdin.readline())
				in_len = len(input)
				instr = ""
				input = input[:in_len-1]
				print(input)
				x = input.split(" ")
				print(x)
				lenx = len(x)
				#should be a switch statement
				if(x[0] == "list"):
					print(record)
				elif(x[0] == "exec"):
					for i in x:
						instr = instr + i + " "
					print(instr)
					send_to_all(instr, connected_list)
					# print("exec")
				elif(x[0] == "file"):
					# filen = "test.txt"
					try:  
						filen = x[1]
						send_file(filen, connected_list)
					except: 
						print("invalid/empty file name")
				


			else:
				# Data from client
				try:
					data = sock.recv(buffer)
					#print "sock is: ",sock
					# data=data1[:data1.index("\n")]
					#print "\ndata received: ",data

					#get addr of client sending the message
					i,p=sock.getpeername()
					if data == b'tata\n':
						msg="\r\33[1m"+"\33[31m "+str(record[(i,p)])+" left the conversation \33[0m\n"
						print(data)
						# send_to_all(sock,str.encode(msg))
						print("Client (%s, %s) is offline" % (i,p)," [",record[(i,p)],"]")
						del record[(i,p)]
						connected_list.remove(sock)
						sock.close()
						continue

					elif not data: 
						(i,p)=sock.getpeername()
						# send_to_all(sock, "\r\33[31m \33[1m"+ str(record[(i,p)])+" left the conversation unexpectedly\33[0m\n")
						print("Client (%s, %s) is offline (error)" % (i,p)," [",record[(i,p)],"]\n")
						del record[(i,p)]
						connected_list.remove(sock)
						sock.close()

					else:
						#decodes message and prints response from client
						data2 = data.decode('utf-8', "backslashreplace")
						print(data2)
				#abrupt user exit
				except:
					(i,p)=sock.getpeername()
					send_to_all(sock, "\r\33[31m \33[1m"+ str(record[(i,p)])+" left the conversation unexpectedly\33[0m\n")
					print("Client (%s, %s) is offline (error)" % (i,p)," [",record[(i,p)],"]\n")
					del record[(i,p)]
					connected_list.remove(sock)
					sock.close()
					continue


	server_socket.close()
