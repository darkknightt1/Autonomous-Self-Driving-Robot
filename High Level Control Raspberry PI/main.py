#main node that directly connect with the low level robot
#subscribe from all relevant nodes and publish to the low level
import rospy
from std_msgs.msg import Bool
import time


speaker_state = True #Intialized by true to make the robot move from the beggining
def speaker_callback(msg):
    global speaker_state 
    speaker_state = msg.data
    publisher.publish(msg.data)#arduino publisher

ultrasonic_state = True #Intialized by true to make the robot move from the beggining
def ultrasonic_callback(msg):
    global ultrasonic_state 
    ultrasonic_state = msg.data
    if speaker_state == True: #if the speaker is telling us to move , solve the case where the robot is at an aruco station and something got infront of him and then moved away
        publisher.publish(msg.data)#arduino publisher


rospy.init_node("main_node")
publisher=rospy.Publisher(name="/Motor/status",data_class = Bool , queue_size = 10)# ardunio publisher
publisher2=rospy.Publisher(name="/main_killpipe",data_class = Bool , queue_size = 10)  # publishing true will kill all nodes , will be integrated with gui 

rospy.Subscriber("/speaker_main_pipe", Bool, speaker_callback) #received from speaker , receive true to move , false to stop
rospy.Subscriber("/ultrasonic_main_pipe", Bool, ultrasonic_callback)   

time.sleep(3)
publisher.publish(True)#just at the beginning to move the robot


while not rospy.is_shutdown():
    pass