# EV3-IoT-Train
A demo about using LEGO EV3 MicroPython to control a LEGO Train with multiple pBricks

The 'main.py' script works in the LEGO EV3  MicroPyhton environment.

It requires:
+ one or more EV3 pBricks with a medium motor connected to (output) Port.A and
an ultrasonic sensor connected to (input) Port.S1.
+ a Wi-Fi USB dongle
+ a proper connection to Wi-Fi network
+ a MQTT broker since we are using MQTT protocol to transfer messages over the network

Other MQTT clients can also participate. If you want to use an Android phone or tablet I included a short
explanation of my own [LEGO IoT Train dashboard](https://github.com/JorgePe/EV3-IoT-Train/blob/master/mqtt-dash/README.md).

For the script to work we need to set an unique hostname for each EV3 on the network.
This is easy to make from Visual Studio Code using the EV3DEV Device Browser plugin -
a [detailed explanation is included](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname/changehostname.md).

There are freely available MQTT brokers in the Internet. The Mosquitto project offers 'test.mosquitto.org'
but be aware that every message exchanged there will be public and others can (and probably will) read them.

You can install 'mosquitto' on your computer and run your own broker. You can even use another EV3 running
'ev3dev' as your broker as available images (including LEGO version) already include 'mosquitto'.

More details soon.

For now, two demo videos:

+ https://youtu.be/ISHDHECn1Ps

+ https://youtu.be/tcXRyngNJtU

The whole project is beeing explained at my blog: https://ofalcao.pt/blog/series/lego-iot-train
