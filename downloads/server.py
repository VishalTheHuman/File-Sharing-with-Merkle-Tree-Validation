# 22AIE203 Data Structures and Algorithms 2
# End Semester Project - File Transfer and Validation using Merkle Tree

# Batch - B

# Member : 
# Vishal S - CB.EN.U4AIE22157

"""
File Format: 

<Hash Value> 
<File Format> 
<Data> 
"""

import os
import socket
from merkletree import MerkleTree
from cryptography.fernet import Fernet 

KEY = "6tMKbjdPA1q1iic_9gvoYUb6LvlgliL0oBJyvTZbu3U="
BUFFER_SIZE = 100000000

def handleOperation(client_socket):
    addr = client_socket.getpeername()
    print(f"Connection from {addr}\n")

    request_type = client_socket.recv(BUFFER_SIZE).decode()

    if request_type == "1":
        uploadFile(client_socket)
    elif request_type == "2":
        downloadFile(client_socket)

def uploadFile(client_socket):
    file_path = client_socket.recv(BUFFER_SIZE).decode()
    client_socket.sendall("OK".encode())
    file_content = client_socket.recv(BUFFER_SIZE).decode()
    if not file_content:
        return
    os.makedirs("files", exist_ok=True)

    with open("files/" + file_path, "w") as f:
        f.write(file_content)

    print(f"File '{file_path}' uploaded successfully.")
    print(f"\nContent of '{file_path}':\n{file_content}\n")
    hash_value = MerkleTree("files/" + file_path).buildTree()
    data = f"{hash_value}\n{file_path.split('.')[-1]}\n{file_content}"
    MerkleTree.validate(data)


def downloadFile(client_socket):
    file_path = "files/" + client_socket.recv(BUFFER_SIZE).decode()

    if not os.path.exists(file_path):
        client_socket.sendall("File Not Found!".encode())
        client_socket.close()
        print(f"File '{filename}' Not Found!")  # Use 'file_path' instead of 'filename'
        return

    file_content, file_extension = MerkleTree.getContent(file_path)
    hash_value = MerkleTree(file_path).buildTree()
    data = f"{hash_value}\n{file_extension}\n{file_content}"

    fnet = Fernet(KEY)
    MerkleTree.storeRaw(fnet.encrypt(data.encode()).decode(), "server_raw.txt")
    MerkleTree.validate(data)

    print(f"Sending Data for '{filename}'...\n")  # Use 'file_path' instead of 'filename'
    try:
        client_socket.sendall(fnet.encrypt(data.encode()))
        acknowledgment = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received from client: {acknowledgment}\n")
    except Exception:
        print("Client disconnected while sending data.\n")

    client_socket.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    port = 8000
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, _ = server_socket.accept()
            handleOperation(client_socket)
    except KeyboardInterrupt:
        print("Server terminated by user.")

    server_socket.close()

if __name__ == "__main__":
    server()
