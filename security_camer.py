
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017 Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
import grovepi
import time
import paho.mqtt.client as mqtt
import time
import socket


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

ip_address= '172.20.10.10' 
"""your code here"""
#create a client object
client = mqtt.Client()

#attach the on_connect() callback function defined above to the mqtt client
client.on_connect = on_connect


client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

client.loop_start()
time.sleep(1)

#look up MQTT 
# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")


# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4

arr=[i for i in range(3)]
cnt=0
baseline=grovepi.ultrasonicRead(ultrasonic_ranger)

while True:
# Read distance value from Ultrasonic
    try:
        if(grovepi.ultrasonicRead(ultrasonic_ranger) > 60000):
            pass
        else:
            print(grovepi.ultrasonicRead(ultrasonic_ranger))
            arr[cnt] = grovepi.ultrasonicRead(ultrasonic_ranger)

            cnt+=1

            if (cnt==3):
                cnt=0
                avg=sum(arr)/3
                if (avg > (baseline+5)) or (avg < (baseline-5)):
                    # import the opencv library 
                    print("hi")
                    client.publish("shada/security", "Turn on")
    except:
                            pass

    time.sleep(0.1) # don't overload the i2c bus
