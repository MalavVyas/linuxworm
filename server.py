import socket, select, sys

#Function to send message to all connected clients
def send_to_all (message, connected_list):
	#Message not forwarded to server and sender itself
	for socket in connected_list:
		if socket != server_socket:
			socket.send(str(message).encode('utf-8'))
			# try :
			# except :
			# 	print("error in sending message")
				# if connection not available
				# socket.close()
				# connected_list.remove(socket)

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
				if(x[0] == "list"):
					print(record[0])
				elif(x[0] == "exec"):
					for i in x:
						instr = instr + i + " "
					print(instr)
					send_to_all(instr, connected_list)
					# print("exec")
				# if(input == "list"):
				# 	print(record)
				# elif(input[:4] == "exec"):
				# 	print(input[5:4])

			else:
				# Data from client
				try:
					data = str(sock.recv(buffer))
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

					else:
						msg="\r\33[1m"+"\33[35m "+str(record[(i,p)])+": "+"\33[0m"+data+"\n"
						# send_to_all(msg)
						print(data)
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
