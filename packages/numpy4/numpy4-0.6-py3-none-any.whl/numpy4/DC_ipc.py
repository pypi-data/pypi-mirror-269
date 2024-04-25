# ********************************** SERVER *********************************

import socket
import threading
def handle_client(client_socket):
   data = client_socket.recv(1024)
   if not data:
       return
   # Split the received string into individual integers
   received_data = list(map(int, data.decode('utf-8').split(',')))
   print(f"Received integers: {received_data}")
   print(f"Sum of integers: {sum(received_data)}")
   client_socket.close()
def start_server():
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(('0.0.0.0', 8888))
   server.listen(5)
   print("[*] Listening on 0.0.0.0:8888")
   while True:
       client_socket, addr = server.accept()
       print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
       client_handler = threading.Thread(target=handle_client, 
args=(client_socket,))
       client_handler.start()
       
if __name__ == "__main__":
   server_thread = threading.Thread(target=start_server)
   server_thread.start()


# *************************************** CLIENT ************************************************

# client.py
import socket
def send_data(target_ip, target_port, data):
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client.connect((target_ip, target_port))
   # Send integers as a comma-separated string
   data_str = ','.join(map(str, data))
   client.send(data_str.encode('utf-8'))
   client.close()
if __name__ == "__main__":
   print("Enter 4 integers to send to the server:")
   integers_to_send = []
   for i in range(1, 5):
       num = int(input(f"{i}: "))
       integers_to_send.append(num)
   # Simulate sending 4 integers from the client
   send_data('127.0.0.1', 8888, integers_to_send)