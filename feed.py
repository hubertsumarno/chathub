import socket

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
FORMAT = "utf-8"

def main():
    feed_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    feed_socket.connect((IP, PORT))

    client_type = 'f'.encode(FORMAT)
    client_type_header = f"{len(client_type):<{HEADER_LENGTH}}".encode(FORMAT)
    feed_socket.send(client_type_header + client_type)

    while True:
        # Extract username
        username_header = feed_socket.recv(HEADER_LENGTH)
        if not username_header:
            continue
        username_length = int(username_header.decode(FORMAT).strip())
        username = feed_socket.recv(username_length).decode(FORMAT)

        # Extract message
        message_header = feed_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode(FORMAT).strip())
        message = feed_socket.recv(message_length).decode(FORMAT)

        print(f'({username}) > {message}')


if __name__ == '__main__':
    main()