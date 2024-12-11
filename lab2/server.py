# server.py
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import os

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def run_server(host='127.0.0.1', port=8000):
    with SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()

        def upload_file(filename, data):
            """
            Receives a file from the client and saves it to the 'received_files' directory.
            
            :param filename: Name of the file to be saved.
            :param data: Binary data of the file.
            :return: Success or failure message.
            """
            try:
                print(f"Received upload request for file: {filename}")
                data_size = len(data.data)
                print(f"Data size received: {data_size} bytes")

                # Ensure the 'received_files' directory exists
                os.makedirs('received_files', exist_ok=True)
                filepath = os.path.join('received_files', filename)

                # Write binary data to the file
                with open(filepath, 'wb') as f:
                    f.write(data.data)

                print(f"Successfully received and saved file: {filepath}")
                return f"File '{filename}' uploaded successfully."
            except Exception as e:
                print(f"Error receiving file '{filename}': {e}")
                return f"Failed to upload file '{filename}'. Error: {str(e)}"

        # Register the upload_file function so clients can call it
        server.register_function(upload_file, 'upload_file')

        print(f"XML-RPC Server listening on {host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server.")

if __name__ == "__main__":
    run_server()
