import pickle # To serialise the data
import socket # To send and receive data

HEADER_SIZE = 4 # The amount of bytes used to send the size - a maximum message size of 4,294,967,295 bytes can be represented with 32 bits (4 bytes)

# The function used to send binary to the socket
def send_binary(sending_socket, data):
    pickled_data = pickle.dumps(data) # pickle the data - serialise it
    size = len(pickled_data) # Calculate the size of the pickled message
	# Send it to the socket - using + on bytes combines them one after the other.
    sending_socket.send(size.to_bytes(HEADER_SIZE, byteorder="big") + pickled_data)

def get_binary(receiving_socket):
	
	# A list to hold any messages from the buffer
    messages = []

	# Create the buffer, a binary variable
    buffer = b""
    socket_open = True
	# While the socket has data in it - keep repeating
    while socket_open:

        # Yield any messages
        for message in messages:
            yield message
        messages = []

        # Read any data from the socket
        data = receiving_socket.recv(1024)

        # If zero data is returned the socket is closed
        if not data:
            socket_open = False

        # Add the data to the buffer
        buffer += data
        #print(buffer)
        
        processing_buffer = True
        while processing_buffer:
        
            # Have we got a header
            if len(buffer) >= HEADER_SIZE:
                # Get the header
                size = int.from_bytes(buffer[0:HEADER_SIZE], byteorder="big")

                # Have we got a complete message
                if len(buffer) >= HEADER_SIZE + size:
                    # Append the message to the list
                    unpickled_message = pickle.loads(buffer[HEADER_SIZE:HEADER_SIZE + size])
                    messages.append(unpickled_message)
                    # Strip the message from the buffer
                    buffer = buffer[HEADER_SIZE + size:]
                else:
                    # There isnt enough data for this message
                    processing_buffer = False

            else:
                # There isnt enough data for a header
                processing_buffer = False
