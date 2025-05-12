import socket
import struct
import cv2
import numpy as np
from flask import Flask, Response, render_template_string

# Configuration
host = '0.0.0.0'  # Listen on all interfaces
port = 8833       # Port to use for the connection

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

# Buffer to hold the incoming data
data_dict = {}

# Flask app to serve the video stream
app = Flask(__name__)

def gen():
    while True:
        packet, addr = sock.recvfrom(65535)
        
        if len(packet) < 6:
            continue

        # Unpack the header
        frame_id, chunk_id, num_chunks = struct.unpack('!HHH', packet[:6])
        chunk_data = packet[6:]

        if frame_id not in data_dict:
            data_dict[frame_id] = [None] * num_chunks
        
        data_dict[frame_id][chunk_id] = chunk_data

        if all(data_dict[frame_id]):
            # All chunks received, reassemble
            buffer = b''.join(data_dict[frame_id])
            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if frame is not None:
                #cv2.imshow('TUTOBOT VID-stream', frame)
                # Encode frame as JPEG
                _, jpeg = cv2.imencode('.jpg', frame)
                
                frame = jpeg.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            # Remove the frame from the dictionary
            del data_dict[frame_id]

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # HTML content for the main page
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TUTOBOT</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background: url('bg.jpg') no-repeat center center fixed;
                background-size: cover;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
            }
            .content {
                max-width: 80%;
                background-color: rgba(0, 0, 0, 0.5);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }
            .video-stream {
                width: 100%;
                height: auto;
                border: 2px solid white;
                border-radius: 10px;
                margin: 20px 0;
            }
            .description {
                text-align: left;
            }
            h1 {
                margin-bottom: 10px;
            }
            p {
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="content">
            <div class="description">
                <h1>Welcome to TUTOBOT</h1>
                <p>TUTOBOT is an advanced robot designed to revolutionize the experience of visiting museums and art galleries. Acting as a knowledgeable and engaging tour guide, TUTOBOT provides visitors with detailed information about exhibits, art pieces, and historical artifacts. It ensures that every visitor, regardless of their background or prior knowledge, leaves with a deeper understanding and appreciation of the displayed items.</p>
                <img class="video-stream" src="/video_feed" alt="Video Stream">
                <p>TUTOBOT is equipped with advanced AI technology, allowing it to interact with visitors in a natural and intuitive manner. It can answer questions, provide additional context, and even offer personalized recommendations based on the visitor's interests. This makes each tour unique and tailored to the individual.</p>
                <p>TUTOBOT can work in any museum or art gallery and interact with any visitor, thanks to its ability to speak multiple languages. Its computer vision capabilities enable it to identify exhibits and provide relevant information accordingly. Additionally, TUTOBOT is equipped with video streaming capabilities, allowing for real-time monitoring and ensuring smooth operation throughout the tour.</p>
                <p>Whether you are a history buff, an art lover, or just a curious visitor, TUTOBOT is here to guide you through a journey of discovery and learning. Join TUTOBOT on an unforgettable tour and see the museum in a whole new light.</p>
            </div>
        </div>
    </body>
    </html>

    '''
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

    

