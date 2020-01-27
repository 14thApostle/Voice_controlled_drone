#!/usr/bin/env python
import rospy

from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from mavros_msgs.srv import SetMode

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String, Float64
from geometry_msgs.msg import TwistStamped

rospy.init_node('todrone', anonymous=True)
compass_hdg = 0
def compass_get(data):
    global compass_hdg
    # print(data)
    compass_hdg = data.data

rospy.Subscriber("/mavros/global_position/compass_hdg", Float64, compass_get)

def callback(data1):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data1.data)
    data = str(data1.data)
    print(data)
    assign(data)
rospy.Subscriber("/voice", String, callback)

current_pos = PoseStamped()

def current_pos_callback(position):

    global current_pos
    current_pos = position

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
        pos_pub = current_pos
        try:
            pos_pub.pose.position.x = float(d[0])
            pos_pub.pose.position.y = float(d[1])
            pos_pub.pose.position.z = float(d[2])
        except:
            pass

        setpoint_client.publish(pos_pub)

    if(data[0]=='velocity'):
        # Mavros velocity publisher
        setvel_client = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',TwistStamped, queue_size=1)
        d = data[1].split(".")
        velocity_msg = TwistStamped()
        d.extend(['0','0','0'])
        print(d)
        velocity_msg.twist.linear.x = float(d[0])
        velocity_msg.twist.linear.y = float(d[1])
        velocity_msg.twist.linear.z = float(d[2])
        setvel_client.publish(velocity_msg)

    if(data[0]=='spin'):
        # Mavros velocity publisher
        setvel_client = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',TwistStamped, queue_size=1)
        velocity_msg = TwistStamped()
        velocity_msg.twist.angular.z = float(4)
        setvel_client.publish(velocity_msg)

        setyaw_client = rospy.Publisher('/mavros/global_position/compass_hdg',Float64, queue_size=1)
        yaw_msg = Float64()
        yaw_msg.data = compass_hdg
        setyaw_client.publish(yaw_msg)



print(compass_hdg)
rospy.spin()


