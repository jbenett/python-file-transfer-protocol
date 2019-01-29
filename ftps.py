import os
import sys
import socket
import time

# Getting input from command line
PORT = int(sys.argv[1])
trollPort = int(sys.argv[2])

# Define constants
HOST = ''
b = ''
gammaIP = ''
ack = 0
sub_directory = 'FTP'

# Set up socket to listen on port
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSocket.bind((HOST, PORT))
print('Listening for data on port ', PORT)

# Recieve first round of data
package, fluff = serverSocket.recvfrom(1024)
flag, sequenceNumber = package[6], package[7]

while 1:
	while (package == None) or (sequenceNumber != ack) :
		# Resend the expected sequence number
		serverSocket.sendto(sequenceNumber.to_bytes(1, 'big'), (gammaIP, trollPort))
		package, fluff = serverSocket.recvfrom(1024)
		flag, sequenceNumber = package[6], package[7]

	if flag == 1:
		# Get the size of the file
		fileSize = int.from_bytes(package[8:], 'big')
		print('File Size: ', str(fileSize))
		serverSocket.sendto(ack.to_bytes(1, 'big'), (gammaIP, trollPort))
		if ack == 0:
			ack = 1
		else:
			ack = 0

	if flag == 2:
		# Get the file name
		fileName = package[8:].decode('utf-8')
		print('File Name: ', fileName)
		serverSocket.sendto(ack.to_bytes(1, 'big'), (gammaIP, trollPort))
		if not os.path.exists(sub_directory):
			os.makedirs(sub_directory)
		file = open((sub_directory + '/' + fileName), 'wb')
		if ack == 0:
			ack = 1
		else:
			ack = 0
	
	if flag == 3:
		# Write copy
		chunk = package[8:]
		serverSocket.sendto(ack.to_bytes(1, 'big'), (gammaIP, trollPort))
		fileSize = fileSize - len(chunk)
		file.write(chunk)
		if fileSize == 0:
			break
		if ack == 0:
			ack = 1
		else:
			ack = 0
			
file.close()	
serverSocket.close()