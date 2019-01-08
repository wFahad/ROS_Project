#!/usr/bin/env python
# license removed for brevity
import rospy
import math
import actionlib 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import *
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import MapMetaData#bouns

#from math import radians, degrees


global posx,posy,posz,ox,oy,oz,ow

#///////////////////////////////////////////////////////
def x (data):
    global posx, posy
    posx = data.pose.pose.position.x
    posy = data.pose.pose.position.y
#///////////////////////////////////////////////////////
def Room_List():
    print("List Of the Room Numbers:")
    print("'1': Room A1 ")
    print("'2': Room A2 ")
    print("'3': Room A3 ")
    print("'4': Room A4 ")
    print("'5': Room A5 ")
    print("'6': Room A6 ")
    print("'7': Room A7 ")
    print("'8': Room A8 ")
    print("'0': Finsh ")
    print("Please enter your target room number:")

    Room_No = input()
    return Room_No

#///////////////////////////////////////////////////////
def Rooms_Pose():
    A1_X =4.80200374229
    A1_Y =9.01782205587
    A2_X =1.87652554458
    A2_Y =7.24388907684
    A3_X =5.77507106228
    A3_Y =7.26191075421
    A4_X =2.54864903478
    A4_Y =2.75341872886
    A5_X =5.42893996854
    A5_Y =4.47812909509
    A6_X =4.73750010218
    A6_Y =0.608354492354
    A7_X =4.77031544569
    A7_Y =2.06383165944
    A8_X =9.19328092917
    A8_Y =3.87879519416
         
#//////////////////////////////////////////////////////
#AT the START THOE ROBOT WILL GO TO HOME
    move_to_goal(A7_X,A7_Y,7)#call
#//////////////////////////////////////////////////////
#user can select room
    while not rospy.is_shutdown():
        choice = Room_List()#call
        if(choice == 1):
            move_to_goal(A1_X,A1_Y,1)#call
        elif(choice == 2):
            move_to_goal(A2_X,A2_Y,2)#call
        elif(choice == 3):
            move_to_goal(A3_X,A3_Y,3)  #call      
        elif(choice == 4):
            move_to_goal(A4_X,A4_Y,4)#call
        elif(choice == 5):
            move_to_goal(A5_X,A5_Y,5)#call
        elif(choice == 6):
            move_to_goal(A6_X,A6_Y,6)#call
        elif(choice == 7):
            move_to_goal(A7_X,A7_Y,7)#call
        elif(choice == 8):
            move_to_goal(A8_X,A8_Y,8)#call
#//////////////////////////////////////////////////////
def rotate(isClockwise, angle_to_rotate):
    pub = rospy.Publisher('/cmd_val_mux/input/teleop', Twist, queue_size=10)#create pub on the cmd_val_mux&input&teleop topic
    rate = rospy.Rate(10)#set pub rate of 10Hz
    velocity_message = Twist()# create a var name velocity_message of type Twist
    if( isClockwise == True):
        velocity_message.angular.z = -0.5
        pass
    else:
        velocity_message.angular.z = +0.5
        pass
    rate.sleep() 

    t0 = rospy.Time.now().to_sec() 
    currenttangle = 0 
    while(currenttangle < angle_to_rotate): 
        pub.publish(velocity_message)# Send information to the node
        tx = rospy.Time.now().to_sec()
        currenttangle = 0.5 * (tx - t0)
    velocity_message.angular.z = 0
    pub.publish(velocity_message)# Send information to the node
#//////////////////////////////////////////////////////
def motion(c, target_distance):
    global posx,posy
    pub = rospy.Publisher('/cmd_val_mux/input/teleop', Twist, queue_size=10)
    rate = rospy.Rate(10)
    velocity_message = Twist()

    x0 = posx
    y0 = posy

    while not rospy.is_shutdown():
        if( c == True ):
                velocity_message.linear.x = 0.5
                pass
        else:
                velocity_message.linear.x = -0.5
                pass
        rospy.loginfo("Sending a velocity message")
        rospy.loginfo(velocity_message)
        rate.sleep() 
        xt=posx
        yt=posy
        print('{} {}'.format(xt, yt))
        distance = math.sqrt(math.pow((xt-x0,2)+math.pow((yt-y0),2)))
        print distance
        if(distance>target_distance):
            break
    velocity_message.linear.x = 0.0
    pub.publish(velocity_message)
    rate.sleep()
#//////////////////////////////////////////////////////
def move_to_goal(locx , locy , id):
    ac = actionlib.SimpleActionClient("move_base", MoveBaseAction) 
    while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))): 
        rospy.loginfo("waiting ...")

   
    goal=MoveBaseGoal()
    goal.target_pose.header.frame_id="map" 
    goal.target_pose.header.stamp=rospy.Time.now()
    goal.target_pose.pose.position.x = locx
    goal.target_pose.pose.position.y = locy
    goal.target_pose.pose.position.z = 0
    goal.target_pose.pose.orientation.w = 1.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    
    ac.send_goal(goal) 
    ac.wait_for_result(rospy.Duration(60))
    if(ac.get_state()==GoalStatus.SUCCEEDED):
        rospy.loginfo("you have reach goal...")
        rotate(True , 2*math.pi)
        if(id == 2 or id == 3 or id == 4 or id == 5):
            motion(True , 1)
            rotate(True , math.pi)

    else:
        rospy.loginfo("The robot faild to reach the goal...")
        return False
  

if __name__ == '__main__':
    try:
        #rospy.init_node('map_nav_node',anonymous=True)
        rospy.Subscriber('/acml_pose', PoseWithCovarianceStamped,x)#Create a Subscriber to the acml_pose topic
        rospy.init_node('map_nav_node',anonymous=True)#Initiate a node
        Rooms_Pose()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("map_navigation node terminated.")
