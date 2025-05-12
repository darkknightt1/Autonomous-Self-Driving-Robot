#this node subscribe to aruco number and play the crossponding audio file to it
import pygame
import time
import rospy
from std_msgs.msg import Int32 , Bool

audio_files_path = [["rpi_lab/Design/ENG1.mp3","rpi_lab/Design/ENG2.mp3","rpi_lab/Design/ENG3.mp3","rpi_lab/Design/ENG4.mp3","rpi_lab/Design/ENG_Welcome.mp3","rpi_lab/Design/ENG_Bye.mp3"],
                    ["rpi_lab/Design/SP1.mp3","rpi_lab/Design/SP2.mp3","rpi_lab/Design/SP3.mp3","rpi_lab/Design/SP4.mp3","rpi_lab/Design/SP_Welcome.mp3","rpi_lab/Design/SP_Bye.mp3"],
                    ["rpi_lab/Design/FR1.mp3","rpi_lab/Design/FR2.mp3","rpi_lab/Design/FR3.mp3","rpi_lab/Design/FR4.mp3","rpi_lab/Design/FR_Welcome.mp3","rpi_lab/Design/FR_Bye.mp3"],
                    ["rpi_lab/Design/AR1.mp3","rpi_lab/Design/AR2.mp3","rpi_lab/Design/AR3.mp3","rpi_lab/Design/AR4.mp3","rpi_lab/Design/AR_Welcome.mp3","rpi_lab/Design/AR_Bye.mp3"]]
pygame.mixer.init()


#variable that receive the aruco number 
Audio_file_to_Run = -1
Language = -1
welcome_audio = 0
def Audio_callback(msg):
    global Audio_file_to_Run 
    Audio_file_to_Run = msg.data

def Arduino_finish_callback(msg):
    if msg.data == 1:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(audio_files_path[Language][5] ) 
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)     # Adjust tick rate

def Language_callback(msg):
    global Language
    global welcome_audio
    Language = msg.data
    welcome_audio = 1
#kill the node callback function
kill_state = False
def kill_callback(msg):
    global kill_state
    kill_state = msg.data

rospy.init_node("Speakers")
rospy.Subscriber("/GUI_speaker_pipe", Int32, Language_callback)
rospy.Subscriber("/aruco_speaker_pipe", Int32, Audio_callback)
rospy.Subscriber("/arduino_GUI_pipe", Int32, Arduino_finish_callback)
publisher=rospy.Publisher(name="/speaker_main_pipe",data_class = Bool, queue_size = 10)

while True:
    if kill_state == False:
        if Language >= 0 :
            if welcome_audio == 1:
                 if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(audio_files_path[Language][4] ) 
                    pygame.mixer.music.play()
                    publisher.publish(False)             # Stop the robot
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)     # Adjust tick rate
                        
                    welcome_audio = 0
                    #Audio_file_to_Run = -1  # Reset the audio file to run
                    publisher.publish(True)
                        
            if Audio_file_to_Run >= 0 :
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(audio_files_path[ Language ][ Audio_file_to_Run ] ) 
                    pygame.mixer.music.play()
                    publisher.publish(False)             # Stop the robot
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)     # Adjust tick rate 

                    Audio_file_to_Run = -1  # Reset the audio file to run
                    publisher.publish(True) # Run the robot again , audio file has been finished


        else :
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
    else:
        break
    
    time.sleep(0.1)