import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

FORMAT = "utf-8"

# Handles message receiving
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode(FORMAT).strip())

        return client_socket.recv(message_length).decode(FORMAT)
    except:
        return False


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Solves 'socket in-use error'
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((IP, PORT))
    server_socket.listen()

    sockets_list = [server_socket]

    # key: socket object | value: user header and name as data
    messangers = {}
    feeds = set()

    print(f'LIstening for connections on {IP}:{PORT}...')

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            # New connection has been notified
            if notified_socket == server_socket:

                client_socket, client_address = server_socket.accept()
                client_type = receive_message(client_socket)

                if client_type == 'm':

                    user = receive_message(client_socket)
                    messangers[client_socket] = user
                    print(f'Accepted new messanger "{client_address}:{user}" | messanger_count: {len(messangers)}')

                elif client_type == 'f':

                    feeds.add(client_socket)
                    print(f'Accepted new feed {client_address} | feed_count: {len(feeds)}')

                sockets_list.append(client_socket)

            # Received message
            else:

                message = receive_message(notified_socket)

                if message is False:
                    if notified_socket in messangers:
                        print(f'Disconnected messanger "{messangers[notified_socket]}" | messanger_count: {len(messangers) - 1}')
                        del messangers[notified_socket]
                    elif notified_socket in feeds:
                        print(f'A feed disconnected | feed_count: {len(feeds) - 1}')
                        feeds.remove(notified_socket)

                    sockets_list.remove(notified_socket)
                else:
                    user = messangers[notified_socket]
                    print(f'Received message from ({user}): {message}')

                    user_header = f'{len(user):<{HEADER_LENGTH}}'.encode(FORMAT)
                    message_header = f'{len(message):<{HEADER_LENGTH}}'.encode(FORMAT)

                    for feed_socket in feeds:
                        feed_socket.send(user_header + user.encode(FORMAT))
                        feed_socket.send(message_header + message.encode(FORMAT))

        # Precautionary measure to handle some socket exceptions
        for notified_socket in exception_sockets:

            sockets_list.remove(notified_socket)

            if notified_socket in messangers:
                del messangers[notified_socket]
                print(f'Closed messanger from: {messangers[notified_socket]}')
            elif notified_socket in feeds:
                del feeds[notified_socket]
                print(f'Closed feed from: {feeds[notified_socket]}')


if __name__ == '__main__':
    main()