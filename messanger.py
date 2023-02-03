import socket

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
FORMAT = "utf-8"

DISCONNECT_MESSAGE = "!DISCONNECT"

def main():
    messanger_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messanger_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() won't block, just a return some exception we'll handle
    messanger_socket.setblocking(False)

    client_type = 'm'.encode(FORMAT)
    client_type_header = f"{len(client_type):<{HEADER_LENGTH}}".encode(FORMAT)
    messanger_socket.send(client_type_header + client_type)

    my_username = input('Enter Username: ')
    username = my_username.encode(FORMAT)
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode(FORMAT)
    messanger_socket.send(username_header + username)

    while True:
        message = input(f'({my_username}): ')
        
        if message == DISCONNECT_MESSAGE:
            break

        if message:

            message = message.encode(FORMAT)
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode(FORMAT)
            messanger_socket.send(message_header + message)


if __name__ == '__main__':
    main()
    