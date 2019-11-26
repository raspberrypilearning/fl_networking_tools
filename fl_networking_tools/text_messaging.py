import pickle # To serialise the data
import socket # To send and receive data

def send_text(sending_socket, text):
    text = text + "\n"
    data = text.encode()
    sending_socket.send(data)

def get_text(receiving_socket):
    buffer = ""

    socket_open = True
    while socket_open:
        # read any data from the socket
        data = receiving_socket.recv(1024)

        # if no data is returned the socket must be closed
        if not data:
            socket_open = False

        # add the data to the buffer
        buffer = buffer + data.decode()

        # is there a terminator in the buffer
        terminator_pos = buffer.find("\n")
        while terminator_pos > -1:
            # get the message from the buffer
            message = buffer[:terminator_pos]
            # remove the message from the buffer
            buffer = buffer[terminator_pos + 1:]
            # yield the message
            yield(message)
            # is there another terminator in the buffer
            terminator_pos = buffer.find("\n")