# High-Level Control System – TUTOBOT (Raspberry Pi)
This package implements the high-level control architecture for TUTOBOT, an autonomous museum tour robot. It runs on a Raspberry Pi using ROS and coordinates sensor inputs, multimedia feedback, and communication with the central control server.


## The system consists of six ROS Python nodes:

## 1. ultrasonic.py
### Function: Reads data from ultrasonic sensors.

### Publishes: Distance measurements to the robot's safety or obstacle-avoidance modules.

## 2. aruco_reader.py
### Function: Detects and identifies ArUco markers via onboard camera.

### Publishes: Marker index corresponding to museum exhibit location.

3. speaker.py
Function: Plays audio commentary (e.g., exhibit information).

Subscribes to: ArUco marker index.

Executes: Corresponding pre-recorded audio file (e.g., Arabic audio for "Nefertari").

4. videostream.py
Function: Streams live video from the robot’s camera.

Protocol: UDP stream to the Flask web server.

Use: Enables remote users and operators to view the robot's perspective.

5. gui.py
Function: Acts as a communication interface between robot and control GUI at the server.

Publishes: Full robot state (sensor data, position, marker index).

Subscribes to: Operator control commands (e.g., behavior override, manual control).

6. main.py
Function: Central logic controller of the robot.

Subscribes to: Sensor nodes, ArUco data, GUI input.

Publishes to: Low-level embedded controllers to drive robot behavior.
