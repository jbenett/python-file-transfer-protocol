import os
import sys
import socket
import select
import time

# Get user input
gammaIP = str(sys.argv[1])
gammaPort = int(sys.argv[2])
trollPort= int(sys.argv[3])
fileName = str(sys.argv[4])

# Defining Cnstants
timeout = 1.5
HOST = ''
PORT = 4001
header = b''
data = b''
flag = 1
sequenceNumber = 0
CHUNK_SIZE = 1000
gammaIPb = gammaIP.split('.')
i = 0

# Setting up the client socket on localhost with port 4001
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSocket.bind((HOST,PORT))

# Placeholder for required params see https://docs.python.org/2/library/select.html
wlist = []
xlist = []

# System call to obtain filesize
size = os.stat(fileName).st_size

# Create header from remote IP and remote Port that will begin every segment
while i < len(gammaIPb):
	integer = int(gammaIPb[i])
	header = header + integer.to_bytes(1, 'big')
	i = i + 1
header = header + gammaPort.to_bytes(2, 'big')

# Create first datagram to be sent
print('Sending first segment...')
data = header + flag.to_bytes(1, 'big') + sequenceNumber.to_bytes(1,'big') + size.to_bytes(4, 'big')
clientSocket.sendto(data, (gammaIP, trollPort))

while 1:	
	readList, writeList, errorList = select.select([clientSocket], wlist, xlist, timeout)
	ack = int.from_bytes(readList[0].recv(1), 'big')
	if ack != sequenceNumber:
		print('Resending first segment...')
		clientSocket.sendto(data, (gammaIP, trollPort))
	else:
		print('Segment 1 acknowledged!')
		flag = 2
		if sequenceNumber == 1:
			sequenceNumber = 0
		else:
			sequenceNumber = 1
			
		break
		
print('Sending second segment...')
data = header + flag.to_bytes(1, 'big') + sequenceNumber.to_bytes(1,'big') + fileName.encode('utf-8')
clientSocket.sendto(data, (gammaIP, trollPort))

while 1:
	readList, writeList, errorList = select.select([clientSocket], wlist, xlist, timeout)
	ack = int.from_bytes(readList[0].recv(1), 'big')
	if ack != sequenceNumber:
		print('Resending second segment...')
		clientSocket.sendto(data, (gammaIP, trollPort))
	else:
		print('Segment 2 acknowledged!')
		flag = 3
		if sequenceNumber == 1:
			sequenceNumber = 0
		else:
			sequenceNumber = 1
			
		break

print('Sending file...')
file = open(fileName,'rb')

while 1:
	chunk = file.read(CHUNK_SIZE)
	if chunk:
		data = header + flag.to_bytes(1, 'big') + sequenceNumber.to_bytes(1,'big') + chunk
		clientSocket.sendto(data, (gammaIP, trollPort))
		while 1:
			readList, writeList, errorList = select.select([clientSocket], wlist, xlist, timeout)
			ack = int.from_bytes(readList[0].recv(1), 'big')
			if ack != sequenceNumber:
				print('Resending third segment...')
				clientSocket.sendto(data, (gammaIP, trollPort))
			else:
				print('Segment 3 acknowledged!')
				break
			
		if sequenceNumber == 1:
			sequenceNumber = 0
		else:
			sequenceNumber = 1
			
	else:
		break;

clientSocket.close()
file.close()
print('File transfer completed')

