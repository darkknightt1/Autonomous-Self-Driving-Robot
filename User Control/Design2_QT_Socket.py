from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QApplication, QComboBox, QSlider
from PySide6.QtCore import Qt, QTimer, QElapsedTimer, QThread, Signal
import sys
import socket
import threading
import time
import cv2
import numpy as np
import struct
from flask import Flask, Response, render_template_string

global counter 
counter = 0
conn = None
# Flask app to serve the video stream
app = Flask(__name__)

data_dict = {}

def receive_frames(sock):
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
                # Display frame using OpenCV
                cv2.imshow('TUTOBOT Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    button_4.setEnabled(True)
                    break

                # Encode frame as JPEG for streaming
                _, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            # Remove the frame from the dictionary
            del data_dict[frame_id]

    cv2.destroyAllWindows()
    sock.close()

def gen(sock):
    for frame in receive_frames(sock):
        yield frame

@app.route('/video_feed')
def video_feed():
    return Response(gen(sock), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
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
                background: url('YOUR_BACKGROUND_IMAGE_URL') no-repeat center center fixed;
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
                margin-bottom: 20px;
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
            <img class="video-stream" src="/video_feed" alt="Video Stream">
            <div class="description">
                <h1>Welcome to TUTOBOT</h1>
                <p>TUTOBOT is an advanced robot designed to revolutionize the experience of visiting museums and art galleries. Acting as a knowledgeable and engaging tour guide, TUTOBOT provides visitors with detailed information about exhibits, art pieces, and historical artifacts. It ensures that every visitor, regardless of their background or prior knowledge, leaves with a deeper understanding and appreciation of the displayed items.</p>
                <p>TUTOBOT is equipped with advanced AI technology, allowing it to interact with visitors in a natural and intuitive manner. It can answer questions, provide additional context, and even offer personalized recommendations based on the visitor's interests. This makes each tour unique and tailored to the individual.</p>
                <p>TUTOBOT can work in any museum or art gallery and interact with any visitor, thanks to its ability to speak multiple languages. Its computer vision capabilities enable it to identify exhibits and provide relevant information accordingly. Additionally, TUTOBOT is equipped with video streaming capabilities, allowing for real-time monitoring and ensuring smooth operation throughout the tour.</p>
                <p>Whether you are a history buff, an art lover, or just a curious visitor, TUTOBOT is here to guide you through a journey of discovery and learning. Join TUTOBOT on an unforgettable tour and see the museum in a whole new light.</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content)

class FlaskThread(QThread):
    def run(self):
        app.run(host='0.0.0.0', port=8000)

def start_streaming():
    global sock
    host = '0.0.0.0'
    port = 8844
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    for _ in receive_frames(sock):
        pass
 
# Thread class to handle receiving messages from the socket
class SocketReceiverThread(QThread):
    message_received = Signal(str)
    
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        while True:
            try:
                message = self.conn.recv(1024)
                if len(message)>0:
                    messageeee=message.decode("utf-8")
                    print(messageeee)
                    if messageeee == "Tour ended":
                        connection_status_label.setText("<font color='black'>Connected & Tour Ended")
                        station_number_label.setText("<font color='black'>Station Number: Not Set")
                        time.sleep(10)
                        button_1.setEnabled(True) #enable the start button
                        button_3.setDisabled(True) #enable the start button
                        slider.setEnabled(True) #enable the start button
                        combo_box.setEnabled(True) #enable the start button
                    elif messageeee =="0":
                        station_number_label.setText("<font color='black'>Station Number: 1")
                    elif messageeee =="1":
                        station_number_label.setText("<font color='black'>Station Number: 2")
                    elif messageeee =="2":
                        station_number_label.setText("<font color='black'>Station Number: 3")
                    elif messageeee =="3":
                        station_number_label.setText("<font color='black'>Station Number: 4")
                        
                        
                        
                    elif  messageeee =="Obstacle Detected":     
                        robot_state_label.setText(f"Robot State: <font color='RED'> Obstacle Detected")
                    elif  messageeee =="No Obstacle":     
                        robot_state_label.setText(f"Robot State: <font color='GREEN'>No Obstacle")
            except socket.error as e:
                print(f"Socket error: {e}")
                break


# Create a Socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        
        host = ""
        port = 9999
        s = socket.socket()
        s.settimeout(5)  # Set a timeout for socket operations

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        
        print("Binding the Port: " + str(port))
        
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")

# Establish connection with a client (socket must be listening)
def socket_accept():
    global conn, receiver_thread
    
    try:
        conn, address = s.accept()
        print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
        #connection_status_label.setText("Connection established with TUTOBOT.")


        # Start the socket receiver thread
        receiver_thread = SocketReceiverThread(conn)
        receiver_thread.start()
        
    except socket.timeout:
        connection_status_label.setText("<font color='black'>Can't Connect To TUTOBOT,Will Try Again.")
        print("Can't connect to the robot, try again.")


# Send commands to client
def send_command(cmd):
    global conn
    if len(str.encode(cmd)) > 0:
        conn.send(str.encode(cmd))


def handle_received_message(message):
    print(f"Received message: {message}")
    # Save the message or perform other actions here


def button2_clicked():
    print("Awwww2   !")
    button_2.setDisabled(True)#disable the connect button as it has already been connected
    connection_status_label.setText("<font color='black'>Connecting to the robot...")
    create_socket()
    bind_socket_thread = threading.Thread(target = bind_socket_with_timeout)
    bind_socket_thread.start()
    

def button4_clicked():# streaming button
    print("Awwww4   !")
    global counter
    counter+=1
    button_4.setEnabled(False)
    if counter == 1: #only the first time
        #flask_thread = FlaskThread()
        #flask_thread.start()
        pass

    streaming_thread = threading.Thread(target=start_streaming)
    streaming_thread.start()
    
    

def button1_clicked():
    global timer, elapsed_timer 
    global conn
    print("Awwww1   !")
    if conn:  #make sure that Check if connection is established 
        send_command(str(slider_value))
        time.sleep(0.25)
        send_command(combo_box.currentText())#send language
        elapsed_timer.start()  # Start the elapsed timer
        timer.start(1000)      # Start the QTimer to update every second
        # Disable the slider and combo box
        connection_status_label.setText("<font color='black'>Connected & Tour Started")
        slider.setEnabled(False)
        combo_box.setEnabled(False)
        button_1.setDisabled(True)
        button_3.setEnabled(True)
    
def button3_clicked():
    global timer, elapsed_timer 
    global conn
    print("Awwww3   !")
    if conn:  #make sure that Check if connection is established 
        send_command("0")# send speed of zero zero
        time.sleep(0.25)
        
        #elapsed_timer.hasExpired()  # Start the elapsed timer
            
        # Disable 
        connection_status_label.setText("<font color='black'>Connected & Tour Paused")
        button_1.setEnabled(True)    #enable start button
        button_3.setDisabled(True)    #enable start button


def bind_socket_with_timeout():
    global conn
    while True: 
        bind_socket()
        socket_accept()
        if conn:
            button_1.setEnabled(True)#enable the start button to be able to send to the robot
            button_2.setDisabled(True)#disable the connect button as it has already been connected
            button_4.setEnabled(True)
            connection_status_label.setText("<font color='black'Connection established with TUTOBOT.")
            break
           
                


        



def combo_box_changed(index):
    current_text = combo_box.itemText(index)
    print(f"Selected index: {index}, value: {current_text}")
    update_current_state_display(slider_value, current_text)


def slider_value_changed(value):
    global slider_value
    slider_value = value
    print(f"Slider value: {slider_value}")
    update_current_state_display(slider_value, combo_box.currentText())

    

def update_current_state_display(slider_value, combo_text):
    current_state_label.setText(f"<font color='black'>Robot Velocity:<font color='red'> {slider_value}<font color='black'>, Language:<font color='red'> {combo_text}")
    

def update_station_number(station_number):
    station_number_label.setText(f"<font color='black'>Station Number: <font color='green'>{station_number}")


def update_elapsed_time():
    elapsed_time_ms = elapsed_timer.elapsed()
    elapsed_time_s = elapsed_time_ms / 1000
    time_label.setText(f"<font color='black'>Elapsed Time: <font color='green'>{elapsed_time_s:.0f} SEC.")


app = QApplication(sys.argv)
window = QMainWindow()

mainWidget = QWidget()
mainWidget.setObjectName("mainWidget")
mainWidget.setStyleSheet("""
    #mainWidget {
        background-image: url('bg.jpg');
        background-repeat: no-repeat;
        background-position: center;
    }
""")

# Set a custom font
custom_font = QFont("Helvetica Neue", 14)

# Creating buttons
button_1 = QPushButton("START")
button_1.setFont(QFont("Helvetica Neue", 20, QFont.Bold))
button_1.setFixedSize(140, 60)
button_1.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 15px;
        padding: 10px;
    }
    QPushButton:disabled {
        background-color: #9E9E9E;
        color: #E0E0E0;
    }
""")
button_1.clicked.connect(button1_clicked)
button_1.setDisabled(True)

button_2 = QPushButton("CONNECT")
button_2.setFont(QFont("Helvetica Neue", 20, QFont.Bold))
button_2.setFixedSize(160, 60)
button_2.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 15px;
        padding: 10px;
    }
    QPushButton:disabled {
        background-color: #9E9E9E;
        color: #E0E0E0;
    }
""")
button_2.clicked.connect(button2_clicked)

button_3 = QPushButton("STOP")
button_3.setFont(QFont("Helvetica Neue", 20, QFont.Bold))
button_3.setFixedSize(140, 60)
button_3.setStyleSheet("""
    QPushButton {
        background-color: #F44336;
        color: white;
        border-radius: 15px;
        padding: 10px;
    }
    QPushButton:disabled {
        background-color: #9E9E9E;
        color: #E0E0E0;
    }
""")
button_3.clicked.connect(button3_clicked)
button_3.setDisabled(True)

button_4 = QPushButton("VIDSTREAM")
button_4.setFont(QFont("Helvetica Neue", 15, QFont.Bold))
button_4.setFixedSize(140, 60)
button_4.setStyleSheet("""
    QPushButton {
        background-color: blue;
        color: white;
        border-radius: 15px;
        padding: 10px;
    }
    QPushButton:disabled {
        background-color: #9E9E9E;
        color: #E0E0E0;
    }
""")
button_4.clicked.connect(button4_clicked)
button_4.setDisabled(True)

# Creating a QComboBox (drop-down menu)
combo_box = QComboBox()
combo_box.setFont(custom_font)
combo_box.addItems(["English", "Español", "Français", "العربية"])
combo_box.setFixedSize(350, 40)
combo_box.currentIndexChanged.connect(combo_box_changed)
combo_box.setStyleSheet("""
    QComboBox {
        padding: 5px;
        border-radius: 10px;
        background-color: #FFFFFF;
        color: #000000;
    }
""")

# Creating a QSlider
slider_value = 20
slider = QSlider(Qt.Horizontal)
slider.setRange(5, 25)
slider.setValue(slider_value)
slider.setFixedSize(350, 40)
slider.valueChanged.connect(slider_value_changed)
slider.setStyleSheet("""
    QSlider::groove:horizontal {
        height: 8px;
        background: #B0BEC5;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #1E88E5;
        width: 18px;
        height: 18px;
        border-radius: 9px;
        margin: -5px 0;
    }
""")

# Creating QLabels to display the current state, station number, elapsed time, and connection status
current_state_label = QLabel()
current_state_label.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
current_state_label.setFixedSize(1000, 40)
update_current_state_display(slider_value, combo_box.currentText())

station_number_label = QLabel("<font color='black'>Station Number: Not Set")
station_number_label.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
station_number_label.setFixedSize(250, 40)

time_label = QLabel("<font color='black'>Elapsed Time: 0 SEC.")
time_label.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
time_label.setFixedSize(250, 40)

connection_status_label = QLabel("<font color='black'>Connection Status: <font color='red'> Not Connected</font>")
connection_status_label.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
connection_status_label.setFixedSize(400, 40)
connection_status_label.setStyleSheet("font-size: 20px;")

robot_state_label = QLabel("<font color='black'>Robot State: <font color='green'>No Obstacle</font>")
robot_state_label.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
robot_state_label.setFixedSize(350, 40)

# Creating the layout and adding widgets
layout = QVBoxLayout()
layout.setSpacing(20)
layout.setContentsMargins(20, 20, 20, 20)

# Layout for the image and combo box
top_layout = QHBoxLayout()
top_layout.addWidget(combo_box)

layout.addLayout(top_layout)
layout.addWidget(slider)
layout.addWidget(current_state_label)
layout.addWidget(connection_status_label)
layout.addWidget(robot_state_label)

# Create a horizontal layout for the station number label
station_number_layout = QHBoxLayout()
station_number_layout.addStretch()
station_number_layout.addWidget(station_number_label)

layout.addLayout(station_number_layout)

# Create a horizontal layout for the timer label
timer_layout = QHBoxLayout()
timer_layout.addStretch()
timer_layout.addWidget(time_label)

layout.addLayout(timer_layout)

# Create a horizontal layout for the buttons
button_layout = QHBoxLayout()
button_layout.addStretch()
button_layout.addWidget(button_2)
button_layout.addStretch()
button_layout.addWidget(button_1)
button_layout.addStretch()
button_layout.addWidget(button_3)
button_layout.addStretch()
button_layout.addWidget(button_4)
button_layout.addStretch()
layout.addLayout(button_layout)

mainWidget.setLayout(layout)

# QTimer to update the elapsed time every second
timer = QTimer()
timer.timeout.connect(update_elapsed_time)

# QElapsedTimer to track the elapsed time
elapsed_timer = QElapsedTimer()

# Show the main widget
window.setCentralWidget(mainWidget)
window.show()

# Run the application event loop
sys.exit(app.exec())