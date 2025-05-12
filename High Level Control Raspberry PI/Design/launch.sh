#!/bin/bash
source /opt/ros/noetic/setup.bash
# Run Python scripts
roscore &
sleep 10
rosrun rosserial_python serial_node.py /dev/ttyUSB0 &
sleep 5
python3 /home/pi/rpi_lab/Design/aruco.py &
sleep 1
python3 /home/pi/rpi_lab/Design/speakers.py &
sleep 1
python3 /home/pi/rpi_lab/Design/ultrasonic.py &
python3 /home/pi/rpi_lab/Design/main.py &
python3 /home/pi/rpi_lab/Design/ttttt.py &


sleep 1
python3 /home/pi/rpi_lab/Design/videostream.py &
