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

    mode_change_client = rospy.ServiceProxy('mavros/set_mode',SetMode)
    arming_cl = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
    takeoff_client = rospy.ServiceProxy('mavros/cmd/takeoff',CommandTOL)

    setvel_client = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',TwistStamped, queue_size=1)
    setpoint_client = rospy.Publisher('mavros/setpoint_position/local',PoseStamped, queue_size=1)
    setyaw_client = rospy.Publisher('/mavros/global_position/compass_hdg',Float64, queue_size=1)
    
    velocity_msg = TwistStamped()
    pos_pub = current_pos
    yaw_msg = Float64()


    if(data[0]=='take' and data[1]=='off'):
        # Mode Change, Arming, Takeoff
        mode_change_client.call(custom_mode = 'GUIDED')
        arming_cl.call(True)
        takeoff_client.call(altitude=int(data[2]))

    if(data[0]=='direction'):
        d = data[1].split(".")
        try:
            pos_pub.pose.position.x = float(d[0])
            pos_pub.pose.position.y = float(d[1])
            pos_pub.pose.position.z = float(d[2])
        except Exception as e:
            print(e)
        setpoint_client.publish(pos_pub)

    if(data[0]=='velocity'):
        # Mavros velocity publisher
        d = data[1].split(".")
        d.extend(['0','0','0'])
        velocity_msg.twist.linear.x = float(d[0])
        velocity_msg.twist.linear.y = float(d[1])
        velocity_msg.twist.linear.z = float(d[2])
        setvel_client.publish(velocity_msg)


    if(data[0]=='come'):
        velocity_msg.twist.linear.x = 4
        setvel_client.publish(velocity_msg)

    if(data[0]=='go'):
        velocity_msg.twist.linear.x = -4
        setvel_client.publish(velocity_msg)

    if(data[0]=='right'):
        velocity_msg.twist.linear.y = 4
        setvel_client.publish(velocity_msg)

    if(data[0]=='left'):
        velocity_msg.twist.linear.y = -4
        setvel_client.publish(velocity_msg)

    if(data[0]=='ascend'):
        velocity_msg.twist.linear.z = 4
        setvel_client.publish(velocity_msg)

    if(data[0]=='down'):
        velocity_msg.twist.linear.z = -4
        setvel_client.publish(velocity_msg)


    if(data[0]=='spin'):
        velocity_msg.twist.angular.z = float(4)
        setvel_client.publish(velocity_msg)

        yaw_msg.data = compass_hdg
        setyaw_client.publish(yaw_msg)

print(compass_hdg)
rospy.spin()


