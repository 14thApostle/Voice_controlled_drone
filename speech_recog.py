import speech_recognition as sr
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

for i in range(3):
    print("{}th Try".format(i))
    print("You said {}\n\n".format(return_speech()))

