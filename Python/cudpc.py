import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #AF_INET:ipv4 SOCK_DGRAM:udp 

for data in ['Michael', 'Tracy', 'Sarah']:
    s.sendto(data, ('127.0.0.1', 9999))
    print s.recv(1024)

s.close()
