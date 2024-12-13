# server_mpi.py
from mpi4py import MPI
import sys

def receive_file(output_path="received_file_mpi.txt", client_rank=1):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank != client_rank:
        print("Only the designated server process receives files.")
        return

    # Receive file size
    file_size = comm.recv(source=MPI.ANY_SOURCE, tag=11)
    print(f"Receiving file of size: {file_size} bytes.")

    # Prepare buffer
    buffer = bytearray(file_size)

    # Receive the file data
    comm.Recv([buffer, MPI.BYTE], source=MPI.ANY_SOURCE, tag=22)
    print(f"File received. Saving to {output_path}.")

    # Write to file
    with open(output_path, "wb") as f:
        f.write(buffer)
    print(f"File saved as '{output_path}'.")

if __name__ == "__main__":
    receive_file()
