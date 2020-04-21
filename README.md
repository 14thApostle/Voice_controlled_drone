# Voice_controlled_drone
#### Control a drone using simple voice commands.
Right now the supported ones are 
* takeoff
* direction {x} {y} {z}
* velocity {x} {y} {z}
* come
* go 
* right 
* left
* ascend
* down
* spin

Usage 
----
```
roscore
python3 speech_recog.py
python3 speech_drone.py
```
1) speech_recog for voice recognition and publishes the text output to a topic.
2) speech_drone for subscribing the test output from the previous program and to publish position and velocity setpoints accordingly.

Dependencies
---
``` 
sudo apt-get install portaudio19-dev    
sudo apt-get install python-pyaudio python3-pyaudio
pip3 install SpeechRecognition pyaudio
```
