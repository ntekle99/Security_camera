# import the opencv library 
import cv2 
import time
import paho.mqtt.client as mqtt

camera_check=False

def on_connect(client, userdata, flags, rc):


    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe("shada/security")

#Add the custom callbacks by indicating the topic and the name of the callback handle


def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "msg: " + str(msg.payload, "utf-8"))
    global camera_check
    if(str(msg.payload, "utf-8")=="Turn on"):
        camera_check=True


#Custom message callback.



if __name__ == '__main__':
    #create a client object
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) 
    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect


    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

    client.loop_start()

    counter = 0


    while True:
        time.sleep(1)
        if camera_check:
            vid = cv2.VideoCapture(0)
            while True:
                ret, frame = vid.read()
                if not ret:
                    break
                # Encode frame to JPEG
                _, encoded_frame = cv2.imencode('.jpg', frame)
                # Publish the encoded frame
                client.publish("shada/video", encoded_frame.tobytes(), qos=1)
                # Wait for a while before capturing the next frame
                time.sleep(0.1)
                if counter == 100:
                    cv2.imwrite("./ntimage.png", frame)
                counter+=1

            vid.release()
            
