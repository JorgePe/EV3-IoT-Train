# EV3-IoT-Train
A demo about using LEGO EV3 MicroPython to control a LEGO Train with multiple pBricks

The 'main.py' script works in the LEGO EV3  MicroPyhton environment.

It requires one or more EV3 pBricks with a medium motor connected to (output) Port.A and
an ultrasonic sensor conencted to (input) Port.S1.

It also requires a Wi-FI USB dongle and a proper connection to Wi-Fi network.

Since we are using MQTT protocol to transfer messages over the network we also need a MQTT broker.

Other MQTT clients can also participate.

For the script to work we need to set an unique hostname for each EV3 on the network.
This is easy to make from Visual Studio Code using the EV3DEV Device Browser plugin -
a [detailed explanation is included](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname.md).
