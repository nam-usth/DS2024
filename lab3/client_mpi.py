# client_mpi.py
from mpi4py import MPI
import sys

def send_file(file_path, server_rank=0):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == server_rank:
        print("Master process does not send files.")
        return

    # Read the file
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)

    # Send file size
    file_size = len(data)
    comm.send(file_size, dest=server_rank, tag=11)
    print(f"Sent file size: {file_size} bytes to server.")

    # Send the file data
    comm.Send([bytearray(data), MPI.BYTE], dest=server_rank, tag=22)
    print(f"Sent file '{file_path}' to server.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: mpirun -n <number_of_processes> python client_mpi.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    send_file(file_path)
