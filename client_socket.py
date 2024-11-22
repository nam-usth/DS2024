import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))
print("Connected to server.")

file_path = 'dog.jpg'
with open(file_path, 'rb') as file:
    data = file.read(1024)
    while data:
        client_socket.send(data)
        data = file.read(1024)

print("File sent successfully.")
client_socket.close()
