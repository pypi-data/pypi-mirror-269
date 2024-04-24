# ******************************************* SERVER *******************************************

import socket
import threading

def broadcast(message, clients):
   for client in clients:
       try:
           client.send(message.encode('utf-8'))
       except:
           # Handle exceptions if a client connection is no longer valid
           clients.remove(client)

def handle_client(client_socket, clients):
   while True:
       try:
           data = client_socket.recv(1024)
           if not data:
               break
           message = data.decode('utf-8')
           print(f"Received message: {message}")
           broadcast(message, clients)
       except:
           # Handle exceptions if a client connection is no longer valid
           clients.remove(client_socket)
           break
       
def start_server():
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(('0.0.0.0', 8888))
   server.listen(5)
   print("[*] Listening on 0.0.0.0:8888")
   clients = []
   while True:
       client_socket, addr = server.accept()
       print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
       clients.append(client_socket)
       client_handler = threading.Thread(target=handle_client, args=(client_socket, clients))
       client_handler.start()

if __name__ == "__main__":
    start_server()


# ******************************************* CLIENT 1 *******************************************

import socket
import threading

def receive_messages(client_socket):
   while True:
       try:
           data = client_socket.recv(1024)
           if not data:
               break
           message = data.decode('utf-8')
           print(f"\nReceived broadcast: {message}")
       except:
           break
       
def send_message(client_socket):
   while True:
       message = input("Enter message to broadcast (type 'exit' to quit): ")
       if message.lower() == 'exit':
           break
       client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
   client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client1.connect(('127.0.0.1', 8888))
   receive_thread1 = threading.Thread(target=receive_messages, args=(client1,))
   receive_thread1.start()
   send_thread1 = threading.Thread(target=send_message, args=(client1,))
   send_thread1.start()
   receive_thread1.join()
   send_thread1.join()
   client1.close()



# ******************************************* CLIENT 2 *******************************************

import socket
import threading

def receive_messages(client_socket):
   while True:
       try:
           data = client_socket.recv(1024)
           if not data:
               break
           message = data.decode('utf-8')
           print(f"\nReceived broadcast: {message}")
       except:
           break
       
def send_message(client_socket):
   while True:
       message = input("Enter message to broadcast (type 'exit' to quit): ")
       if message.lower() == 'exit':
           break
       client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
   client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client2.connect(('127.0.0.1', 8888))
   receive_thread2 = threading.Thread(target=receive_messages, args=(client2,))
   receive_thread2.start()
   send_thread2 = threading.Thread(target=send_message, args=(client2,))
   send_thread2.start()
   receive_thread2.join()
   send_thread2.join()
   client2.close()
