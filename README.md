# ```File Sharing with Merkle Tree Validation```

![Merkle Tree](https://github.com/VishalTheHuman/File-Sharing-with-Merkle-Tree-Validation/assets/117697246/3ab14a15-25a3-4925-8855-7d3634862297)

## Description 📚

This project implements a basic file transfer and validation system using a Merkle Tree. The system follows a client-server architecture, allowing users to upload files from the client to the server and download files from the server to the client. The Merkle Tree is employed to ensure the integrity of the transferred data.

## Components ⚙️

1. **Server:**
   - Listens for incoming client connections on a specified host and port.
   - Handles file upload and download requests from the client.
   - Utilizes a Merkle Tree for file validation and stores uploaded files in the "files" directory.

2. **Client:**
   - Connects to the server and initiates file upload or download based on user input.
   - Sends files to the server for upload or requests files from the server for download.
   - Implements a basic user interface for interaction.

3. **Merkle Tree:**
   - Implements a Merkle Tree structure for generating hash values and validating file content integrity.
   - Provides methods for building the tree, generating hash values, and validating data.

4. **File Format:**
   - Files are formatted with three sections: Hash Value, File Format, and Data.
   - The Merkle Tree is used to validate the integrity of these sections.

## Usage 👥

1. **Server Setup:**
   - Run the `server.py` script on the server machine.
   - The server will start listening for client connections.

2. **Client Setup:**
   - Run the `client.py` script on the client machine.
   - Follow the prompts to choose between uploading and downloading files.
   - Provide the necessary file information as requested.

3. **Merkle Tree:**
   - The `merkletree.py` script contains the implementation of the Merkle Tree used for data integrity validation.

## File Transfer Process 💻

### Upload Process:

   - The client sends a filename to the server, which responds with an acknowledgment.
   - If the acknowledgment is received successfully, the client sends the file content.
   - The server stores the file in the "files" directory, prints the content, generates a hash value using the Merkle Tree, and validates the data integrity.

### Download Process:

   - The client sends a filename to the server.
   - The server checks if the file exists, generates a hash value using the Merkle Tree, and sends the hash value, file format, and content to the client.
   - The client validates the received data integrity using the Merkle Tree and prints the status.

## Dependencies 

   - The system uses the `cryptography` library for Fernet encryption and `hashlib` for hashing.   

   ```bash
   pip install cryptography
   ```  
   ```bash
   pip install hashlib
   ```
