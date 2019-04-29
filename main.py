#!/usr/bin/env pybricks-micropython

##
# Author: Jorge Pereira (C)2019

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.tools import print, wait

# using two extra MicroPython libraries:
# 'umqtt' for MQTT messages between different EV3 through an external broker
from umqtt.robust import MQTTClient
# 'os' to identify the hostname of each EV3
import os

# Scenario: LEGO IoT Train
# The Train uses a 4DBrix WiFi Controller
# Two EV3 work simultaneously as LEFTMOST and RIGHTMOST Masters
# - one ultrasonic sensor on Input 1 ('Port.S1') to prevent collision
# - one medium motor on Output A ('Port.A') to choose the Train's speed
# other MQTT clients can also participate

STARTUP = 1000       # pause (ms) at start
DISTANCE_SAFE = 200  # distance (mm) to stop or reverse the Train
DEBOUNCE = 125       # wait this time (ms) after each button is pressed (empyrical)
WAIT_TRAIN = 50      # wait for Train (4DBrix) to receive command (empyrical)
INITSpeed = 320      # initial speed of our Train (you choose)
MAXSpeed = 1023      # maximum speed accepted by 4DBrix WiFi Controller
MOTORSpeed = 1024    # speed to use with EV3 motor (360 = 1 turn/sec)
TOLERANCE = 4        # acceptable tolerance when reading motor position
SETTLE = 250         # time (ticks) for the user to change motor position before 
                     # considering it done (empyrical)

# Hostnames
RIGHTMOST = 'iota'
LEFTMOST = 'alpha'

us = UltrasonicSensor(Port.S1)
m = Motor(Port.A)

m.reset_angle(0)
print('Motor Reset')
# motor will be used to read speed so defining scale
SCALE = round(360/MAXSpeed, 2)
m.run_target(MOTORSpeed,round(INITSpeed*SCALE), Stop.COAST)   # show initial speed


# Possible hostnames - use your own
RIGHTMOST = 'iota'
LEFTMOST = 'alpha'

# get hostname to use as MQTT_ClientID and decide roles
# LEFTMOST should be at LEFT or F extreme
# RIGHTMOST should be at RIGHT or B extreme

os.system('hostname > /dev/shm/hostname.txt')
file = open('/dev/shm/hostname.txt', 'r')
MQTT_ClientID = file.readline().rstrip('\n')
file.close()
os.system('rm /dev/shm/hostname.txt')

# MQTT definitions:
# we need an external MQTT broker; can use your own by installing 'mosquitto' on your
# computer or a Raspberry Pi or even another EV3 running ev3dev (already installed);
# or can use public brokers available on the Internet but be carefull that all messages
# can be read by others
MQTT_Broker = '192.168.1.87'
#MQTT_Broker = '10.26.10.127'
#MQTT_Broker = 'test.mosquitto.org'
# we use 5 topics:
MQTT_Topic_Status = 'JorgePe/Status'         # for debug only
MQTT_Topic_Train = 'JorgePe/Train'           # to share Train commands
MQTT_Topic_Speed = 'JorgePe/Speed'           # to share Train speed
MQTT_Topic_BFMode = 'JorgePe/BFMode'         # to share Train Back and Forward flag
MQTT_Topic_4DBrix = 'nControl/4DB2'          # to control the 4DBrix WiFi Controller
                                             # '4DB2' is the 'Alias' defined with nControl tool

# Messages
# Train Commands: (S)top (F)orward (B)ackward
TRAIN_STOP = 'S'
TRAIN_FORW = 'F'
TRAIN_BCKW = 'B'
# Back and Forward: (T)rue (F)alse
BFMODE_TRUE = 'T'
BFMODE_FALSE = 'F'

# all EV3 start with same values and from now on they must get them always from the broker 
Status = ''
Train = TRAIN_STOP
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
        if str(msg.decode('utf-8')) == BFMODE_TRUE:
            BackAndForth = True
        elif str(msg.decode('utf-8')) == BFMODE_FALSE:
            BackAndForth = False

client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()
client.set_callback(getmessages)

client.publish(MQTT_Topic_Status, MQTT_ClientID + ' joined')
client.subscribe(MQTT_Topic_Status)
client.subscribe(MQTT_Topic_Train)
client.subscribe(MQTT_Topic_BFMode)
client.subscribe(MQTT_Topic_Speed)

# dangerous - might start a storm
# all EV3 should be settled before changing values
client.publish(MQTT_Topic_Train, Train)
if BackAndForth:
    client.publish(MQTT_Topic_BFMode, BFMODE_TRUE)
else:
    client.publish(MQTT_Topic_BFMode, BFMODE_FALSE)

client.publish(MQTT_Topic_Speed, str(Speed))
m.run_target(MOTORSpeed,round(Speed*SCALE), Stop.COAST)

nDebounce = 0
nSettle = 0

#debug
client.publish(MQTT_Topic_Status, MQTT_ClientID + ' started')    
wait(STARTUP)


while True:
    # check for messages
    client.check_msg()

    # check for new Train commands
    if NewTrain:
        if Train == TRAIN_STOP:
            client.publish(MQTT_Topic_4DBrix, 'mot,s')
        elif Train == TRAIN_FORW:
            client.publish(MQTT_Topic_4DBrix, 'mot,f,'+str(Speed))
        elif Train == TRAIN_BCKW:
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
            client.publish(MQTT_Topic_Train, TRAIN_FORW)
        elif Button.RIGHT in b:
            client.publish(MQTT_Topic_Train, TRAIN_BCKW)
        elif Button.CENTER in b:
            # Stop is processed immediately
            client.publish(MQTT_Topic_4DBrix, 'mot,s')
            client.publish(MQTT_Topic_Train, TRAIN_STOP)
        elif Button.UP in b:
            client.publish(MQTT_Topic_BFMode, BFMODE_TRUE)
        elif Button.DOWN in b:
            client.publish(MQTT_Topic_BFMode, BFMODE_FALSE)

    # check for Train nearby
    d = us.distance()
    if d < DISTANCE_SAFE:
        if Train in [TRAIN_FORW,TRAIN_BCKW]:
            # train is moving
            if (Train == TRAIN_FORW and MQTT_ClientID == LEFTMOST) or \
                (Train == TRAIN_BCKW and MQTT_ClientID == RIGHTMOST) :
                # train is moving this direction
                if BackAndForth == False:
                    # Just Stop
                    client.publish(MQTT_Topic_Train, TRAIN_STOP)
                    Train = TRAIN_STOP
                    NewTrain = True
                else:
                    # Move opposite direction
                    if Train == TRAIN_FORW:
                        client.publish(MQTT_Topic_Train, TRAIN_BCKW)
                        Train = TRAIN_BCKW
                        NewTrain = True
                    else:
                        client.publish(MQTT_Topic_Train, TRAIN_FORW)
                        Train = TRAIN_FORW
                        NewTrain = True
            else :
                # train is moving away so don't care
                pass
        else:
            # train is already stopped so don't care
            pass

    # check for new Speed setting
    if nSettle > 0:
        nSettle = nSettle - 1
        if nSettle == 0:
            client.publish(MQTT_Topic_Speed, str(round(m.angle()/SCALE)))        
        else:
            pass
    else:
        curPosition = m.angle()
        delta = abs(Speed*SCALE - curPosition)
        if delta > TOLERANCE:        
            # new speed value received or user rotated the motor axle
            if NewSpeed:
                m.run_target(MOTORSpeed,round(Speed*SCALE), Stop.COAST)
                NewSpeed = False
            else:
                nSettle = SETTLE # wait user choice to settle
        else:
            NewSpeed = False
                    