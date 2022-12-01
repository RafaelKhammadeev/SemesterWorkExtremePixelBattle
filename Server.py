import socket
from time import sleep


class Server:
	def __init__(self, address):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(address)
		self.sock.listen(1)

	def start(self):
		client, address = self.sock.accept()
		msg = "welcome"
		while 1:
			self.send(client, msg)
			# msg = self.recv()
			# sleep(1)

	def send(self, client, msg):
		client.send(msg.encode('utf-8'))

	def recv(self):
		return self.sock.recv(1024).decode('utf-8')


address = ("127.0.0.1", 10000)
server = Server(address)
server.start()
