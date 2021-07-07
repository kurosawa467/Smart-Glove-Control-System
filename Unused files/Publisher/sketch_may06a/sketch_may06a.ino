#include "PubSubClient.h"
#include "WiFi.h"

const char* ssid = "WG01";
const char* wifi_password = "321losgehts";

const char* mqtt_server = "192.168.178.100";
const char* button_topic = "button";
const char* motion_topic = "motion";
const char* mqtt_username = "mosquitto";
const char* mqtt_password = "mosquitto";
const char* clientID = "ESP32";
const int pushButton = 32;
int previous_button_state = LOW;

WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient);

void connect_WiFi() {
  Serial.print("ESP32 is trying to connect to ");
  Serial.println(ssid);

  WiFi.begin(ssid, wifi_password);

  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}
  
void connect_MQTT() {
  Serial.println("Trying to connect to MQTT broker");
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT broker");
  } else {
    Serial.println("Connection failed");
  }
}

void sendButtonPushedMessage() {
  Serial.println("Button pushed down");
  char* buttonPushedMessage = "1: Button pushed";
  if (client.publish(button_topic, buttonPushedMessage)) {
    Serial.println("Button pushed message sent to MQTT broker");
  } else {
    Serial.println("Button pushed message failed to send to MQTT broker. Reconnecting...");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10);
    client.publish(button_topic, buttonPushedMessage);
  }
}

void sendMotionDetectedMessage() {
  Serial.println("Motion detected.");
  char* motionDetectedMessage = "0: Motion detected";
  if (client.publish(motion_topic, motionDetectedMessage)) {
    Serial.println("Motion detected message sent to MQTT broker");
  } else {
    Serial.println("Motion detected message failed to send to MQTT broker. Reconnecting...");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10);
    client.publish(motion_topic, motionDetectedMessage);
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pushButton, INPUT);
  connect_WiFi();
  connect_MQTT();
}

void loop() {
  // connect_MQTT();
  if (!client.connected()) {
    connect_MQTT();
  }
  client.loop();
  
  Serial.setTimeout(5000*60);
  int push_button_state = digitalRead(pushButton);
  
  if (push_button_state == HIGH) {
    if (previous_button_state == LOW) {
      sendButtonPushedMessage();
      delay(500);
      previous_button_state = HIGH;
    }
  } else {
    if (previous_button_state == HIGH) {
      previous_button_state = LOW;
    }
  }
}
