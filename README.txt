Below is an example of how to run the program with the indicated port numbers.
The client port number is HARDCODED and must be 4001 or it will not work

Client 
4001
Server
4002
Troll Beta
4003
Troll Gamma
4004

Server
python3 ftps.py 4002 4004

Troll 1
troll -C 127.0.0.1 -S 127.0.0.1 -a 4001 -b 4002 4003 -t -x 0

Troll 2
troll -C 127.0.0.1 -S 127.0.0.1 -a 4002 -b 4001 4004 -t -x 0

Client
python3 ftpc.py 127.0.0.1 4002 4003 help.txt