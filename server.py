import socket
import threading

host = '127.0.0.1'
port =56789
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients=[]
names =[]

def broadcast(message):
    for client in clients:
        client.send(message)
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.pop(index)
            client.close()
            broadcast(f'{names[index]} has left the chat room!'.encode('utf-8'))
            names.pop(index)
            break

def receive():
    while True:

        print('server is running')
        client,address = server.accept()
        print(f'connection is established with{str(address)}')
        client.send('Ping?'.encode('utf-8'))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)
        print(f'Welcome to the chat room {name}'.encode('utf-8'))
        broadcast( name+' has joined to room \n'.encode('utf-8'))
        client.send('you are now connected'.encode('utf-8'))
        thread  = threading.Thread(target = handle_client,args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()