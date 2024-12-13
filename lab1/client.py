import socket

def send_file(file_path, host='127.0.0.1', port=65432):
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        
        # Open and send the file
        with open(file_path, "rb") as file:
            while chunk := file.read(1024):  # Read file in chunks
                client_socket.sendall(chunk)
        print(f"File '{file_path}' sent to the server.")

if __name__ == "__main__":
    file_path = input("Enter the path to the file you want to send: ")
    send_file(file_path)
