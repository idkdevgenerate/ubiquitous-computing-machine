import socket
import threading
import random
import time
import os

import hashlib
from collections import defaultdict

from Crypto.Cipher import AES
import base64
from flask import Flask, request, jsonify

# Key and IV for AES encryption (must be 16, 24, or 32 bytes long)
KEY = b"thisisaverysecurekey1234"
IV = b"thisisaninitvector"

def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    encrypted = cipher.encrypt(data)
    return base64.b64encode(encrypted)

def decrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    decrypted = cipher.decrypt(base64.b64decode(data))
    return decrypted

# Function to generate random delays and obfuscate traffic patterns
def obfuscate_traffic(data):
    time.sleep(random.uniform(0.1, 0.5))  # Add random delay
    return data[::-1]  # Reverse the data as a simple obfuscation

def handle_client(client_socket):
    # Receive encrypted and obfuscated data from the client
    encrypted_request = client_socket.recv(1024)
    obfuscated_request = decrypt_data(encrypted_request)
    request = obfuscate_traffic(obfuscated_request)

    # Simulate cloud gaming by streaming a video file
    video_file = "sample_game_stream.mp4"
    if os.path.exists(video_file):
        with open(video_file, "rb") as f:
            while chunk := f.read(4096):
                obfuscated_chunk = obfuscate_traffic(chunk)
                encrypted_chunk = encrypt_data(obfuscated_chunk)
                client_socket.send(encrypted_chunk)

    client_socket.close()

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(("0.0.0.0", random.randint(10000, 60000)))  # Bind to a random high port
    port = proxy_socket.getsockname()[1]
    print(f"Proxy server listening on port {port}")

    proxy_socket.listen(5)

    while True:
        client_socket, addr = proxy_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

app = Flask(__name__)

@app.route('/proxy', methods=['POST'])
def proxy_request():
    try:
        # Extract the target URL and data from the request
        target_url = request.json.get('url')
        data = request.json.get('data', '')

        if not target_url:
            return jsonify({"error": "URL is required"}), 400

        # Forward the request to the target URL
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = target_url.split(':') if ':' in target_url else (target_url, 80)
        server_socket.connect((host, int(port)))
        server_socket.send(data.encode())

        # Get the response from the remote server
        response = server_socket.recv(4096).decode()
        server_socket.close()

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    threading.Thread(target=start_proxy).start()  # Start the proxy server in a separate thread
    app.run(host="0.0.0.0", port=5000)  # Start the Flask API server