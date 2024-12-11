# Read multiple client and close server when say stop
import socket
import threading

def start_server(host='127.0.0.1', port=65432):
    def handle_clients():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()
            print(f"Server listening on {host}:{port}")
            
            while not stop_server_event.is_set():  # Run until stop_server_event is triggered
                try:
                    conn, addr = server_socket.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        with open("received_file.txt", "wb") as file:
                            while True:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                file.write(data)
                        print("File received and saved as 'received_file.txt'")
                except socket.error:
                    break
    
    # Start a thread to handle client connections
    threading.Thread(target=handle_clients, daemon=True).start()
    
    # Wait for the "stop" command
    while True:
        command = input("Type 'stop' to shut down the server: ").strip().lower()
        if command == 'stop':
            stop_server_event.set()
            print("Shutting down the server...")
            break

if __name__ == "__main__":
    stop_server_event = threading.Event()  # Event to signal server shutdown
    start_server()
