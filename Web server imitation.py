from socket import *
import os
from threading import Thread



def SendFile(client):
    files = os.listdir()
    received = client.recv(1024).decode()
    received_split = received.split(' ')
    print('received : \n', received_split[:3])
    name, ext = os.path.splitext(received_split[1])
    name = name[1:]
    if name + ext in files:
        script = "HTTP/1.1 200 OK\r\n"        
        if ext == '.html':
            filepath = name + ext
            contentType = 'text/html'
            with open(filepath, 'r') as f:
                script += "Content-Type: " + contentType + "\r\n"
                script += "\r\n"
                script += f.read()
                script += "\r\n\r\n"
                client.sendall(script.encode())
                print('sent : ', filepath)
        else :
            filepath = name + ext
            contentType = 'image/' + ext[1:]
            with open(filepath, 'rb') as f:
                script += "Content-Type: " + contentType + "\r\n"
                script += "\r\n"
                client.sendall(script.encode())
                bdata = f.read()
                client.sendall(bdata)
                client.sendall("\r\n\r\n".encode())
                print('sent : ', filepath)
    else:
        client.sendall('HTTP/1.1 404 Not Found\n'.encode())

serverPort = 10080
server = socket(AF_INET, SOCK_STREAM)
host = gethostbyname(getfqdn())
server.bind((host, serverPort))
print("website : http://"+ host + ":" + str(serverPort))
print('The TCP server is ready to receive.', host)
server.listen(5)

while True:
    client, (clientHost, clientPort) = server.accept()
    th = Thread(target = SendFile, args=(client,))
    th.start()
    
    
        
    