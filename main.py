#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.tools import print, wait

from umqtt.robust import MQTTClient
import os

STARTUP = 500
DISTANCE_SAFE = 200
DEBOUNCE = 125   # time to prevent multiple keys
PROPAGATE = 100
WAIT_TRAIN = 50
INITSpeed = 320
MAXSpeed = 1023
MOTORSpeed = 1024 # 360 = 1 turn/sec
TOLERANCE = 8  # speed
SETTLE = 500

us = UltrasonicSensor(Port.S1)
m = Motor(Port.A)

m.reset_angle(0)
print('Motor Reset')
# motor will be used to read speed so defining scale
SCALE = round(360/MAXSpeed, 2)
m.run_target(MOTORSpeed,round(INITSpeed*SCALE), Stop.COAST)   # show initial speed


# get hostname to use as MQTT_ClientID and decide roles
# 'alpha' should be at LEFT or F extreme
# 'iota' should be at RIGHT or B extreme

os.system('hostname > /dev/shm/hostname.txt')
file = open('/dev/shm/hostname.txt', 'r')
MQTT_ClientID = file.readline().rstrip('\n')
file.close()
os.system('rm /dev/shm/hostname.txt')

MQTT_Broker = '192.168.1.87'
#MQTT_Broker = '10.26.10.127'
MQTT_Topic_Status = 'JorgePe/Status'
MQTT_Topic_Train = 'JorgePe/Train'
MQTT_Topic_Speed = 'JorgePe/Speed'
MQTT_Topic_BFMode = 'JorgePe/BFMode'
MQTT_Topic_4DBrix = 'nControl/4DB2'

# all EV3 start with same values and from now on they must get them always from the broker 
Status = ''
Train = 'S'     # (S)top (F)orward (B)ackward
NewTrain = False
Speed = INITSpeed
NewSpeed = False
BackAndForth = False
NewButton = False

# callback message to process messages on subscribed topic
def getmessages(topic, msg):
    global Status, Train, NewTrain, Speed, NewSpeed, BackAndForth

    if topic == MQTT_Topic_Status.encode():
        Status = str(msg.decode('utf-8'))
    elif topic == MQTT_Topic_Train.encode():
        s = str(msg.decode('utf-8'))
        if Train != s:
            Train = s
            NewTrain = True
    elif topic == MQTT_Topic_Speed.encode():
        Speed = int(str(msg.decode('utf-8')))
        NewSpeed = True        
    elif topic == MQTT_Topic_BFMode.encode():
        if str(msg.decode('utf-8')) == 'T':
            BackAndForth = True
        elif str(msg.decode('utf-8')) == 'F':
            BackAndForth = False

client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()
client.set_callback(getmessages)

client.publish(MQTT_Topic_Status, MQTT_ClientID + ' listening')
client.subscribe(MQTT_Topic_Status)
client.subscribe(MQTT_Topic_Train)
client.subscribe(MQTT_Topic_BFMode)
client.subscribe(MQTT_Topic_Speed)

# dangerous - might start a storm
# all EV3 should be settled before changing values
client.publish(MQTT_Topic_Train, Train)
if BackAndForth:
    client.publish(MQTT_Topic_BFMode, 'T')
else:
    client.publish(MQTT_Topic_BFMode, 'F')

client.publish(MQTT_Topic_Speed, str(Speed))
m.run_target(MOTORSpeed,round(Speed*SCALE), Stop.COAST)

nDebounce = 0
nSettle = 0

wait(STARTUP)

while True:
    # check for messages
    client.check_msg()

    # check for new Train commands
    if NewTrain:
        if Train == 'S':
            client.publish(MQTT_Topic_4DBrix, 'mot,s')
        elif Train == 'F':
            client.publish(MQTT_Topic_4DBrix, 'mot,f,'+str(Speed))
        elif Train == 'B':
            client.publish(MQTT_Topic_4DBrix, 'mot,b,'+str(Speed))
        NewTrain = False
        wait(WAIT_TRAIN)

    # check for new pressed buttons
    if nDebounce > 0:
        nDebounce = nDebounce - 1
        wait(1)
    elif any(brick.buttons()):
        nDebounce = DEBOUNCE
        b = brick.buttons()
        if Button.LEFT in b:
            client.publish(MQTT_Topic_Train, 'F')
        elif Button.RIGHT in b:
            client.publish(MQTT_Topic_Train, 'B')
        elif Button.CENTER in b:
            # Stop is processed immediately
            client.publish(MQTT_Topic_4DBrix, 'mot,s')
            client.publish(MQTT_Topic_Train, 'S')
        elif Button.UP in b:
            client.publish(MQTT_Topic_BFMode, 'T')
        elif Button.DOWN in b:
            client.publish(MQTT_Topic_BFMode, 'F')

    # check for Train nearby
    d = us.distance()
    if d < DISTANCE_SAFE:
        if Train in ['F','B']:
            # train is moving
            if (Train == 'F' and MQTT_ClientID == 'alpha') or \
                (Train == 'B' and MQTT_ClientID == 'iota') :
                # train is moving this direction
                if BackAndForth == False:
                    # Just Stop
                    client.publish(MQTT_Topic_Train, 'S')
                    Train = 'S'
                    NewTrain = True
                else:
                    # Move opposite direction
                    if Train == 'F':
                        client.publish(MQTT_Topic_Train, 'B')
                        Train = 'B'
                        NewTrain = True
                    else:
                        client.publish(MQTT_Topic_Train, 'F')
                        Train = 'F'
                        NewTrain = True
            else :
                # train is moving away so don't care
                pass
        else:
            # train is already stopped so don't care
            pass

    # check for new Speed setting
    if nSettle > 0:
        nSettle = nSettle -1
        if nSettle == 0:
            LocalSpeed = round(m.angle()/SCALE)      
            client.publish(MQTT_Topic_Speed, str(LocalSpeed))        
            wait(PROPAGATE) # wait user choice to propagate
        else:
            wait(1)
    else:
        LocalSpeed = round(m.angle()/SCALE)
        delta = abs(LocalSpeed - Speed)
        if delta > TOLERANCE:
            # new speed value received or user rotated the motor axle
            if NewSpeed:
                m.run_target(MOTORSpeed,round(Speed*SCALE), Stop.COAST)
                NewSpeed = False
            else:
                nSettle = SETTLE # wait user choice to settle
                    
    
client.publish(MQTT_Topic_Status, MQTT_ClientID + ' completed')
client.disconnect()