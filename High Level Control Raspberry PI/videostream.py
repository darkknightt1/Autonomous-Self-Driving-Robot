import cv2
import socket
import numpy as np
import struct

# Configuration
host = '192.168.1.15'  # IP address of the receiver
port = 8844          # Port to use for the connection


# Configuration
host2 = '192.168.1.15'  # IP address of the receiver
port2 = 8833          # Port to use for the connection


# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (host, port)

# Initialize socket
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr2 = (host2, port2)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Unique identifier for each frame
frame_id = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Encode the frame as JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    buffer = buffer.tobytes()

    # Split the buffer into smaller chunks
    chunk_size = 65000  # Slightly less than the max UDP packet size
    num_chunks = -(-len(buffer) // chunk_size)  # Ceiling division
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, len(buffer))
        chunk = buffer[start:end]
        
        # Pack the header with frame_id, chunk_id, and num_chunks
        header = struct.pack('!HHH', frame_id, i, num_chunks)
        message = header + chunk

        # Send each chunk
        sock.sendto(message, addr)
        
        # Send each chunk
        sock2.sendto(message, addr2)
        
        # Introduce a small delay to avoid overwhelming the network
        cv2.waitKey(1)

    frame_id += 1

cv2.destroyAllWindows()
cap.release()
sock.close()