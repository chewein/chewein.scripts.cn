from wsgiref.simple_server import make_server
from hello import application 

serverUrl=''
serverPort=8000
https = make_server(serverUrl,serverPort,application)
print 'Servring HTTP on port %s...'%(serverPort)
https.serve_forever()