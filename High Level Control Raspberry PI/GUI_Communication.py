import socket
import os
import subprocess
import rospy
from std_msgs.msg import Int32 , Bool
import time

#s = socket.socket()
host = '192.168.1.15'
port = 9999
ultrasonic=0
sideIRs=0
while True:
    try:
        s = socket.socket()
        s.connect((host, port))
        break
    except socket.error as e:
        s.close()
        time.sleep(0.1)
        
        

def arduino_callback(msg): #Receive arduino state for line follower send to GUI
    global ultrasonic
    if msg.data == 2:
        s.send(str.encode("No line detected"))
    elif msg.data == 1:
        s.send(str.encode("Tour ended"))
        
    elif msg.data == 0:
        s.send(str.encode("No Obstacle"))
        
        
    elif msg.data == 3: #ultrasonics are reading ,should stop
        s.send(str.encode("Obstacle Detected"))
        
        
        
def ultrasonic_callback(msg): #Receive Ultrasonic state send to GUI
    global sideIRs
    if msg.data == 1:
        s.send(str.encode("No Obstacle"))
    
    elif msg.data == 0:
        s.send(str.encode("Obstacle Detected"))
        
    
def station_no_callback(msg): #Receive Ultrasonic state send to GUI
    s.send(str.encode(str(msg.data+1)))
    
    
rospy.init_node("GUIII_node")
publisher=rospy.Publisher(name="/GUI_speaker_pipe",data_class = Int32 , queue_size = 10)
publisher_2=rospy.Publisher(name="/GUI_arduino_pipe",data_class = Int32 , queue_size = 10)
rospy.Subscriber("/arduino_GUI_pipe", Int32, arduino_callback)
rospy.Subscriber("/ultrasonic_main_pipe", Bool, ultrasonic_callback)
rospy.Subscriber("/aruco_speaker_pipe",Int32,station_no_callback)

counter = 0

while True:
    try:
        try:
            data = s.recv(1024)
            if (len(data) > 0) :  
                received = data.decode("utf-8")
          
                if received == "English" :
                    publisher.publish(0)
                elif received == "Español" :
                    publisher.publish(1)
                elif received == "Français" :
                    publisher.publish(2)
                elif received == "العربية" :
                    publisher.publish(3)
                    
                    
                else :#Speed to publish to arduino
                    print("publishing to arduino")
                    publisher_2.publish( int(received) )
                
            #s.send(str.encode("receivedddd"))

                print(received)
            
        except socket.timeout:
            print ("timeout")
            
          
    except ConnectionResetError:
        while True:
            try:
                s = socket.socket()
                s.connect((host, port))
                break
            
            except socket.error as e:
                s.close()
                time.sleep(0.1)
        
