#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from mavros_msgs.msg import CommandBool
from mavros_msgs.msg import CommandTOL
from mavros_msgs.msg import SetMode
from geometry_msgs.msg import PoseStamped

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def assign(data):
    data.split("delimiter")
    print(data[0])
    if(data[0]=='take' and data[1]=='off'):
        arm_cmd=CommandBool()
        points=CommandTOL()
        mod=SetMode()
        mode_change_client = rospy.Publisher('mavros/set_mode',SetMode, queue_size=10)
        arming_client = rospy.Publisher('mavros/cmd/arming',CommandBool, queue_size=10)
        takeoff_client = rospy.Publisher('mavros/cmd/takeoff',CommandTOL, queue_size=10)
        mod.request.custom_mode=(char)(48+mode)
	    mode_change_client.call(mod)
        arm_cmd.request.value = True
	    arming_client.call(arm_cmd)
        points.request.altitude=int(data[2],10)
        takeoff_client.call(points)

    if(data[0]=='points'):
        pos_pub = PoseStamped()
        #setpoint_client = nh.advertise<geometry_msgs::PoseStamped>("mavros/setpoint_position/local",200,true)
        setpoint_client = rospy.Publisher('mavros/setpoint_position/local',PoseStamped, queue_size=10)
        pos_pub.pose.position.x = int(data[1],10)
	    pos_pub.pose.position.y = int(data[2],10)
	    pos_pub.pose.position.z = int(data[3],10)
	    pos_pub.pose.orientation.x = 0.0
	    pos_pub.pose.orientation.y = 0.0
	    pos_pub.pose.orientation.z = 0.0
	    pos_pub.pose.orientation.w = 1.0
        setpoint_client.publish(pos_pub)


def listener():
    rospy.init_node('todrone', anonymous=True)

    rospy.Subscriber("voice_cammands", String, callback)
    print(data)
    assign(data)
    rospy.spin()
    
if __name__ == '__main__':
    listener()


