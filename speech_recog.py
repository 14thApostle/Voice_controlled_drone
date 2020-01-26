import speech_recognition as sr
import rospy
from std_msgs.msg import String

print(sr.__version__)

def return_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Speak up")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    print("recognizing")
    data = r.recognize_google(audio)
    print(data)
    return data

#while True:
def talker():
    pub = rospy.Publisher('voice_cammands', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        print("You said {}\n\n".format(return_speech()))
        pub.publish(return_speech())
        rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except:
        pass