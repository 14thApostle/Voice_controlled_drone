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

rospy.init_node('talker', anonymous=True)
pub = rospy.Publisher('/voice', String,queue_size=10)

#while True:
def talker():
    text = return_speech()
    print("You said {}\n\n".format(text))
    pub.publish(text)

while True:
    try:
        talker()
    except Exception:
        print(Exception)
        pass