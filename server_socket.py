import socket
from PIL import Image

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(1)
print("Server listening on port 5000...")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

with open('received.jpg', 'wb') as file:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file.write(data)

print("Received !!!")
client_socket.close()
server_socket.close()

img = Image.open('received.jpg')
grayscale_img = img.convert('L')
grayscale_img.save('received.jpg')

