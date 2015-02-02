import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #AF_INET:ipv4 SOCK_STREAM:tcp 
s.connect(('www.sina.com.cn',80))
s.send('GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnction: close\r\n\r\n')

buffer = []

while True:
    d = s.recv(1024) # the max recv byte one time 
    if d:
        buffer.append(d)
    else:
        break
		
data = ''.join(buffer)

s.close()

# split the http header and data 
header, html = data.split('\r\n\r\n', 1)
print header

with open('sina.html', 'wb') as f:
    f.write(html)
