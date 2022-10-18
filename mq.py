import random
import time
from paho.mqtt import client as mqtt_client
import keyboard
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
broker = '194.5.195.209' #endpoint
port = 9501
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
global velo
global angel
# username = 'emqx'
# password = 'public'
properties=Properties(PacketTypes.PUBLISH)
properties.MessageExpiryInterval=30

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def sendvelo(client, velo): #for sending a velocoty value to mqtt server 
    velotopic = "VR/rover/control/velamout"
    result = client.publish(velotopic, velo)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"current velocity is {velo}")
    else:
        print(f"Failed to send message to topic {topic}")
def sendangel(client, angel): # for sending angel amount to mqtt server 
    velotopic = "VR/rover/control/velangle"
    result = client.publish(velotopic, angel)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"current angel is {angel}")
    else:
        print(f"Failed to send message to topic {topic}")
def run():
    client = connect_mqtt()
    client.loop_start()
    # keyboard.add_hotkey('up', incvelo(client, velo))
    # keyboard.add_hotkey('down', decvelo(client, velo))
    velo = 0
    angel = 0;
    veloref = 0.1
    angref = 0.1;

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            if velo == 2 :      
                print("velocity amount is maximum can not proceed");
                continue          
            velo += veloref;
            velo = round(velo, 1)
            sendvelo(client, velo)
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            if velo == -2:
                print("velocity amount is maximum can not proceed")
                continue
            velo -= veloref;
            velo = round(velo, 1)
            sendvelo(client, velo)
        if event.event_type == keyboard.KEY_DOWN and event.name == 'left':
            if angel == -40 :      
                print("angel amount is maximum can not proceed");
                continue          
            angel -= angref;
            angel = round(angel, 1)
            sendangel(client, angel)
        if event.event_type == keyboard.KEY_DOWN and event.name == 'right':
            if angel == 40:
                print("angel amount is maximum can not proceed")
                continue
            angel += angref;
            angel = round(angel, 1)
            sendangel(client, angel)
        if event.event_type == keyboard.KEY_DOWN and event.name == 's':
            if velo == 0:
                print("rover is stopped right now, wont proceed")
                continue
            velo = 0;
            sendvelo(client, velo)
            print("rover stopped")
        if event.event_type == keyboard.KEY_DOWN and event.name == 'a':
            if angel == 0:
                print("rover angel is 0 right now, wont proceed")
                continue
            angel = 0
            sendangel(client, angel)
            print("angel resseted")
        if event.event_type == keyboard.KEY_DOWN and event.name == 'r':
            velo = 0
            angel = 0
            sendvelo(client, velo)
            sendangel(client, angel)
            print("rover resseted")
        if event.event_type == keyboard.KEY_DOWN and event.name == 'f':

            velo = 0;
            sendvelo(client, velo)
            print("rover stopped by force")

if __name__ == '__main__':
    run()
