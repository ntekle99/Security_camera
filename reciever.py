import cv2 
import numpy as np
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))
    client.subscribe("shada/video")

def on_message(client, userdata, msg):
    # Convert received message to numpy array
    nparr = np.frombuffer(msg.payload, np.uint8)
    # Decode the JPEG frame
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Display the frame
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

if __name__ == '__main__':
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_forever()
