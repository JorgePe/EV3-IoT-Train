# How to change EV3 hostname with Visual Studio Code

1. Use EV3DEV Device Browser to open a SSH Terminal:
![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname01.png)

You will be greated with a command line shell:
![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname02.png)

2. Run 'ev3dev-config' tool:

Since this tool can change system configurations we need to run it with superuser privileges:
```
sudo ev3dev-config
```
![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname03.png)

You will need to give the password for the default user 'robot' (it's 'maker'):

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname04.png)

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname05.png)

3. On the intial menu choose 'Advanced Options':

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname06.png)

then 'A1 Hostname'

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname07.png)

4. You receive e a warning about the rules for hostnames:

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname08.png)

5. Just choose a new hostname and then OK

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname09.png)

you  will return to the initial menu:

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname10.png)

6. Now just disconnect from your EV3DEV:

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname11.png)

7. If you now try to connect to a different EV3DEV device it should show up with the new hostname
and if you open a new SSH Terminal you see the new hostname:

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname12.png)

![](https://github.com/JorgePe/EV3-IoT-Train/blob/master/changehostname13.png)
