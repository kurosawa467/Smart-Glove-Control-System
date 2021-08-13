# Smart Glove Control System

An Internet of Things (IoT) system can be abstracted as a group of connected sensors and actuators, and engineers have been exploring different methods to control them. Some controlling methods have already been widely adapted, for example, letting the user to directly enter a command on a central management portal, or making use of sensors to detect environment factors and adjust actuators accordingly. However, there are scenarios where such methods are not adaptive. For example, when a person with limited motion functionality wishes to control IoT devices, the command inputting method might not be so user-friendly.

In this project, we explore a new way for controlling IoT devices. We aim to come up with an intuitive and easy-to-use controlling method using the glove as a wearable device. To fulfill the requirement of this class, the computation would be conducted in an edge computing component.
Additionally, we should provide test IoT devices to test our prototype, and for demonstration purposes as well.

# Setup
Our project is structured the following:  
- ESP32 microcontroler as glove
- ESP8266 microcontroller as controllable IoT device
- Raspberry Pi as Message Broker and to recognize the performed gestures.
We are using MQTT as communication protocol and we are following the publisher-subscriber pattern. Where the glove publishes new commands, the broker recieves them. Interpretes the gesture (if a gesture is performed) and the publishes again a new message. The IoT device then recieves it if it is subscribed to the according topic.

## The ESP32
There are two kind of sensors connected to the ESP32. An IMU and four flexensors.
The wiring is as follows:

<img src="./Reports and Documents/Glove-circuit.png" width="400px">

The code is developed using the Arduino environment.

## The ESP8266
This ESP has 2 LEDs connected to it. One LED is considered as analoge LED while the second as digital, because our ESP8266 did not provide enough PWM pins. Therefor the LEDs are connected ass follows:

Analog LED:
- Red pin: 14
- Green Pin: 12
- Blue Pin: 15

Digital LED:
- Red pin: 5
- Green Pin: 4
- Blue Pin: 0

## Raspberry Pi setup
We followed this tuorial to set up the mosquitto server on the raspberry pi https://diyi0t.com/microcontroller-to-raspberry-pi-wifi-mqtt-communication/. In Addition to the 1883 port we also added the 1884 port for being able to access the webapp. In total we added the following lined to the etc/mosquitto/mosquitto.conf file:

    password_file /etc/mosquitto/pwfile

    listener 1883
    protocol mqtt 

    listener 1884
    protocol websockets



# Instructions on how it could be run
1. Change internet connection configurations in the ".\Project\Publisher\gloveESP32\WifiAccess.h" and upload code ".\Project\Publisher\gloveESP32\gloveESP32.ino" to the glove microcontroller (ESP32). Keep microcontroller wired up and running.
2. Change internet connection configurations in the ".\Project\Subscriber\LED_Device\WifiAccess.h" and upload code ".\Project\Subscriber\LED_Device\LED_Device.ino" to the LED lights microcontroller (ESP8266). Keep microcontroller wired up and running.
3. Run the Raspberry Pi. First, run command "sudo systemctl start mosquitto". Then navigate to directory "\smart-glove-control-system\Project\Broker", setup the Raspberry Pi IP adress in the code in communication.py, and run it using "python3 communication.py".
4. Run the JavaScripe web app ".\Project\Subscriber\mqtt_web_app\index.html" in your browser.
5. Now everything should be set up and ready to go.


