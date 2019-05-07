The EV3 IoT Train Dashboard

I like to use ['MQTT Dash'](https://play.google.com/store/apps/details?id=net.routix.mqttdash) to create nice MQTT dashboards on my Android devices. It's very easy to use and offers several types of widgets that suit my needs.

For my EV3 LEGO IoT Train dashboard I added 5 widgets:

![Dashboard](https://github.com/JorgePe/EV3-IoT-Train/blob/master/mqtt-dash/mqttdash-01.jpg)

For this I only needed two type of widgets:

- a 'Range/progress' for 'Speed'
- 4 'Switch/button' for 'Forward', 'Stop', 'Backward' and 'B&F'


The 'Range/progress' widget works like an analog 'dial' button, showing the current value in a graphical
way and and also allowing us to change it.

![Speed Dial](https://github.com/JorgePe/EV3-IoT-Train/blob/master/mqtt-dash/mqttdash-02.jpg)

We just configure the proper topic ('JorgePe/Speed') and the range ('0.0' to '1023.0' with a precision '0'
meaning no decimal digits) and a progress color that suites our style preferences.


The 'Switch/button' widget in this dashboard is configured as a button for the 'Forward' / 'Backward' /
'Stop' controls and as a switch for the 'B&F' mode.

To use as a button, we chose the same payload and icon for the 'On' and 'Off' states:

![Forward Button](https://github.com/JorgePe/EV3-IoT-Train/blob/master/mqtt-dash/mqttdash-03.jpg)

so the payloads will be:

- 'F' for the 'Forward' button
- 'S' for the 'Stop' button
- 'B' for the 'Backward' button

and the icons will be the ones that we find more conveniant from the dozens available (too bad we cannot import
our owns but there are really lots of usefull included with the App)

And to use as a switch we chose different patloads and icons for the 'On' and 'Off' states:

- 'T' for 'True' meaning the Train should move 'Back and Forth'
- 'F' for 'False' meaning the Train should stop when reaching and end of the track

![Back'n Forth Switch](https://github.com/JorgePe/EV3-IoT-Train/blob/master/mqtt-dash/mqttdash-04.jpg)
