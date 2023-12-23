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

import socket
from merkletree import MerkleTree
from cryptography.fernet import Fernet 

KEY = "6tMKbjdPA1q1iic_9gvoYUb6LvlgliL0oBJyvTZbu3U="
BUFFER_SIZE = 100000000

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.56.1'
    port = 8000
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}\n")
    request_type = ""
    
    while request_type != "1" and request_type !="2":
        request_type = input("Do you want to upload or download a file?\n (1) Upload\n (2) Download \nEnter : ")
    filename = ""
    
    if request_type == "1":
        filename = input("Enter File Location : ")
    elif request_type == "2":
        filename = input("Enter File Name : ")
    
    client_socket.sendall(request_type.encode())

    if request_type == "1":
        uploadFile(client_socket, filename)
    elif request_type == "2":
        downloadFile(client_socket, filename)

def uploadFile(client_socket, filename):
    client_socket.sendall(filename.encode())
    acknowledgment = client_socket.recv(BUFFER_SIZE).decode()
    if acknowledgment == "OK":
        try:
            with open(filename, "r") as f:
                file_content = f.read()
                client_socket.sendall(file_content.encode())
            print(f"File '{filename}' uploaded successfully.\n")
        except Exception:
            print("Error Uploading the File....")
            client_socket.close()
            return
    else:
        print(f"Server rejected the file upload.\n")


def downloadFile(client_socket, filename):
    client_socket.sendall(filename.encode())

    data = client_socket.recv(BUFFER_SIZE).decode()
    print("Data Received\nValidating the Data...\n")

    if data == "File Not Found!":
        print("File doesn't exist\n")
        client_socket.close()
        return

    try:
        MerkleTree.storeRaw(data, "client_raw.txt")
        fnet = Fernet(KEY)
        data = fnet.decrypt(data).decode()
        status = MerkleTree.validate(data, "downloads/"+".".join(filename.split(".")[:-1]))
        message = "File received successfully" if status else "File validation failed"

        print("\n" + message + "\n")

        acknowledgment = "Received and validated" if status else "Validation failed"
        client_socket.sendall(acknowledgment.encode())
    except Exception as e:
        print(f"Error during file download: {e}\n")

    client_socket.close()

if __name__ == "__main__":
    client()
