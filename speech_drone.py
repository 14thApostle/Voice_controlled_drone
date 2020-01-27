#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from mavros_msgs.srv import SetMode
from geometry_msgs.msg import PoseStamped 
from mavros import command
data =  ""


rospy.init_node('todrone', anonymous=True)

def callback(data1):
    global data
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data1.data)
    data = str(data1.data)
    print(data)
    assign(data)

rospy.Subscriber("/voice", String, callback)



def assign(data):
    data = data.split(" ")
    print(data[0])
    if(data[0]=='take' and data[1]=='off'):
        arm_cmd=CommandBool()
        points=CommandTOL()

        mod = SetMode()
        mod.custom_mode = str(52)
        # mode_change_client = rospy.Service('mavros/set_mode',SetMode)

        # Mode Change
        mode_change_client = rospy.ServiceProxy('mavros/set_mode',SetMode)

        # Arming 
        arming_cl = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
        arming_cl.call(True)

        # Takeoff 
        takeoff_client = rospy.ServiceProxy('mavros/cmd/takeoff',CommandTOL)
        takeoff_client.call(altitude=int(data[2]))

        # mode_change_client(0,52)
        # arm_cmd.request.value = True
        # arming_client.call(arm_cmd)
        # points.request.altitude = int(data[2],10)
        # takeoff_client.publish(points)

    if(data[0]=='direction'):
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


    
# if __name__ == '__main__':
    # listener()
rospy.spin()


