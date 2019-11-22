import pickle
import socket

HEADER_SIZE = 4

def send_binary(sending_socket, data):
    pickled_data = pickle.dumps(data)
    size = len(pickled_data)
    sending_socket.send(size.to_bytes(HEADER_SIZE, byteorder="big") + pickled_data)

def get_binary(receiving_socket):

    messages = []

    buffer = b""
    socket_open = True
    
    while socket_open:

        # yield any messages
        for message in messages:
            yield message
        messages = []

        # read any data from the socket
        data = receiving_socket.recv(1024)

        # if zero data is returned the socket is closed
        if not data:
            socket_open = False

        # add the data to the buffer
        buffer += data
        #print(buffer)
        
        processing_buffer = True
        while processing_buffer:
        
            # have we got a header
            if len(buffer) >= HEADER_SIZE:
                # get the header
                size = int.from_bytes(buffer[0:HEADER_SIZE], byteorder="big")

                # have we got a complete message
                if len(buffer) >= HEADER_SIZE + size:
                    # append the message to the list
                    unpickled_message = pickle.loads(buffer[HEADER_SIZE:HEADER_SIZE + size])
                    messages.append(unpickled_message)
                    # strip the message from the buffer
                    buffer = buffer[HEADER_SIZE + size:]
                else:
                    # there isnt enough data for this message
                    processing_buffer = False

            else:
                # there isnt enough data for a header
                processing_buffer = False