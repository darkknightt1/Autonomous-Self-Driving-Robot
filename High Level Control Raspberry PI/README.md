# High-Level Control System – TUTOBOT (Raspberry Pi)
This package implements the high-level control architecture for TUTOBOT, an autonomous museum tour robot. It runs on a Raspberry Pi using ROS and coordinates sensor inputs, multimedia feedback, and communication with the central control server.


## The system consists of six ROS Python nodes:
## ultrasonic.py
reads ultrasonic sensor data and publishes distance values for obstacle detection and local navigation safety.

## aruco.py
detects ArUco markers via camera input and publishes the corresponding index to localize the robot within the museum.

## speakers.py
subscribes to the ArUco index and plays the matching pre-recorded audio file (e.g., exhibit information in Arabic) via onboard speakers.

## videostream.py
captures camera frames and streams them to the server over UDP, supporting both remote operator monitoring and online museum tours.

## GUI_Communication.py
communicates bidirectionally with the central GUI, publishing robot state (e.g., location, sensor status) and receiving control commands from the operator.

## main.py
acts as the system integrator, subscribing to all relevant topics and sending motion and behavior commands to the low-level robot controller.

## launch.sh
launch all relevant nodes along with roscore
