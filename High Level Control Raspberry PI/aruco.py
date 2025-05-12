import numpy as np
import cv2.aruco as aruco
import cv2 as cv

import rospy
from std_msgs.msg import Int32 , Bool

#kill the node callback function
kill_state = False
def kill_callback(msg):
    global kill_state
    kill_state = msg.data
    


rospy.init_node("aruco_node")
publisher=rospy.Publisher(name="/aruco_speaker_pipe",data_class = Int32, queue_size = 10) 
rospy.Subscriber("/main_killpipe", Bool, kill_callback)

counter = 0
repeated_id = -1 #any intial value , to avoid sending same id twice
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)


cap = cv.VideoCapture(2)

while cap.isOpened():
    #read from the camera the frame and the return value (0/1) to make sure it is working 
    ret, frame = cap.read()
    cv.imshow('frame',frame)
    # Detect markers in the image
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict)
 
    if ids is not None:
        if ids[0][0] != repeated_id:
            counter+=1
            print (counter ,": ",ids[0][0])
            if ids[0][0] < 5:
                publisher.publish(ids[0][0])

        repeated_id =  ids[0][0]   
        





    if cv.waitKey(1) == ord('q')  or kill_state == True :
        break

# Release everything if job is finished
cap.release()
cv.destroyAllWindows()
