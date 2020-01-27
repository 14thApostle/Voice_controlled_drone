#!/usr/bin/env python
import rospy

from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from mavros_msgs.srv import SetMode

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

rospy.init_node('todrone', anonymous=True)

def callback(data1):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data1.data)
    data = str(data1.data)
    print(data)
    assign(data)
rospy.Subscriber("/voice", String, callback)
current_height = 0
def current_pos_callback(position):

    global current_height
    current_height=position.pose.position.z

rospy.Subscriber('mavros/local_position/pose',PoseStamped,current_pos_callback)

def assign(data):
    data = data.split(" ")
    print(data)

    if(data[0]=='take' and data[1]=='off'):
        # Mode Change
        mode_change_client = rospy.ServiceProxy('mavros/set_mode',SetMode)
        mode_change_client.call(custom_mode = 'GUIDED')

        # Arming 
        arming_cl = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
        arming_cl.call(True)

        # Takeoff 
        takeoff_client = rospy.ServiceProxy('mavros/cmd/takeoff',CommandTOL)
        takeoff_client.call(altitude=int(data[2]))

    if(data[0]=='direction'):

        # Mavros local position publisher
        setpoint_client = rospy.Publisher('mavros/setpoint_position/local',PoseStamped, queue_size=1)

        d = data[1].split(".")
        print(d[0])
        print(current_height)

        pos_pub.pose.position.x = float(d[0])
        pos_pub.pose.position.y = float(d[1])
        if d[2]=='':
            pos_pub.pose.position.z = current_height
        else:
            pos_pub.pose.position.z = float(d[2])

        pos_pub.pose.position.z = float(d[2])
        pos_pub.pose.orientation.x = 0.0
        pos_pub.pose.orientation.y = 0.0
        pos_pub.pose.orientation.z = 0.0
        pos_pub.pose.orientation.w = 1.0
        setpoint_client.publish(pos_pub)
rospy.spin()


