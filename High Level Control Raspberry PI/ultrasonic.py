import RPi.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Bool

rospy.init_node("ultrsonic_node")
publisher=rospy.Publisher(name="/ultrasonic_main_pipe",data_class = Bool, queue_size = 10) 

GPIO.setmode(GPIO.BCM)
IR_Left = 6
IR_Right = 26

previous = True


GPIO.setup(IR_Left, GPIO.IN)
GPIO.setup(IR_Right, GPIO.IN)



print("Distance Measurement In Progress")

try:
    while True:
        time.sleep(0.25)
        if  GPIO.input(IR_Left)==GPIO.LOW or GPIO.input(IR_Right)==GPIO.LOW:
            state=False
        else:
            state=True
        
        if state!= previous:
            publisher.publish(state)
            previous = state
            
            
        
finally:
    GPIO.cleanup()
