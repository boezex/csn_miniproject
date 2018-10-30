from time import sleep
import paho.mqtt.client as mqtt
import gpiozero

status = 0
# status 0 = disarmed, status 1 = armed, status 2 =...
sensor = gpiozero.Button(2)
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/domo")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if str(msg.payload) == "disarm":
        global status
        status = 0
    if str(msg.payload) == "arm":
        global status
        status = 1

#Start of the program
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("boezemail.nl", 1883, 60)

client.loop_start()

while True:
    while status == 1:
        if sensor.is_pressed:
            client.publish("/domo","triggered")
            sleep(1)