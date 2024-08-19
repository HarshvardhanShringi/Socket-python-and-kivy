import socket

host = ""  # Server's IP address
port =               # Server's port number

client = socket.socket()  # Create a socket object

try:
    # Connect to the server
    client.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Loop to continuously send messages
    while True:
        # Get input from the user
        message = input("Enter message to send to server (type 'exit' to quit): ")

        if message.lower() == 'exit':
            break  # Exit the loop and close the connection

        # Send the message to the server
        client.send(message.encode())

        # Receive response from the server
        data = client.recv(1024).decode()
        print(f"Received from server: {data}")

finally:
    # Close the connection
    client.close()
