# TUTOBOT Operator & Web Interface
This program enables robot's operator control and public interaction with TUTOBOT, an autonomous museum guide robot. It integrates a PySide6-based GUI for robot supervision and a Flask web server for public video streaming.

## System Overview
Operator GUI (Qt6 / PySide6):

Real-time control of robot behavior.

Embedded MJPEG video streaming.

Socket-based command/feedback interface.

UI elements for robot configuration and state tracking.

## Web Server (Flask):

Live robot video streaming for on-site and remote users.

Intended for tourists inside the museum or online ticket holders.

Accessible via browser; independent from the GUI.

## Video Stream Receiver:

Receives fragmented UDP frames from robot camera.

Reconstructs frames for GUI and web output.

## Architecture

TCP Socket: Bidirectional robot-GUI communication.

Multithreaded Execution: Ensures GUI responsiveness and concurrent streaming.

## Execution 
Start the main operator GUI
 QT_Socket.py

(Optional) Launch the public web server if needed
 Flask_Webserver.py
