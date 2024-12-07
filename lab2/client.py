# client.py
import xmlrpc.client
import os

def send_file(file_path, server_host='127.0.0.1', server_port=8000):
    """
    Sends a file to the XML-RPC server.

    :param file_path: Path to the file to be sent.
    :param server_host: Server's hostname or IP address.
    :param server_port: Server's port number.
    """
    try:
        # Establish connection to the XML-RPC server
        proxy = xmlrpc.client.ServerProxy(f'http://{server_host}:{server_port}/RPC2')
        print(f"Connected to XML-RPC Server at {server_host}:{server_port}")

        # Verify that the file exists
        if not os.path.isfile(file_path):
            print(f"Error: File not found - {file_path}")
            return

        # Read the file in binary mode
        with open(file_path, 'rb') as f:
            file_data = f.read()
        print(f"Read {len(file_data)} bytes from file '{file_path}'")

        filename = os.path.basename(file_path)
        print(f"Uploading file: {filename}")

        # Create a Binary object to send binary data
        binary_data = xmlrpc.client.Binary(file_data)
        print(f"Binary data size to send: {len(binary_data.data)} bytes")

        # Call the remote method 'upload_file'
        response = proxy.upload_file(filename, binary_data)
        print(f"Server response: {response}")

    except xmlrpc.client.ProtocolError as err:
        print(f"Protocol error: {err.errcode} - {err.errmsg}")
    except xmlrpc.client.Fault as fault:
        print(f"XML-RPC Fault: {fault.faultString}")
    except ConnectionRefusedError:
        print(f"Could not connect to server at {server_host}:{server_port}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    file_path = input("Enter the path to the file you want to send: ").strip()
    send_file(file_path)
