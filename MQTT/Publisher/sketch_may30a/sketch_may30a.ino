#include "PubSubClient.h"
#include "WiFi.h"

const char* ssid = "WG01";
const char* wifi_password = "321losgehts";

const char* mqtt_server = "192.168.178.100";
const char* button_topic = "/esp32/button";
const char* flex_topic = "/esp32/flex";
const char* mqtt_username = "mosquitto";
const char* mqtt_password = "mosquitto";
const char* clientID = "ESP32";

const int BUTTON = 32;
const int FLEX = 33;
int previous_button_state = LOW;
const float VCC = 3.3;
const float R_DIV = 47000.0;
const float R_FLAT = 30000.0;
const float R_BENT = 80000.0;
int previous_flex_state = HIGH;

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
    delay(100);
    client.publish(button_topic, buttonPushedMessage);
  }
}

void sendFlexSensorMessage() {
  Serial.println("Flex sensor bending detected.");
  char* flexDetectionMessage = "0: Flex sensor is bent";
  if (client.publish(flex_topic, flexDetectionMessage)) {
    Serial.println("Flex detection message sent to MQTT broker");
  } else {
    Serial.println("Flex detection message failed to send to MQTT broker. Reconnecting...");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(100);
    client.publish(flex_topic, flexDetectionMessage);
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(BUTTON, INPUT);
  pinMode(FLEX, INPUT);
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
  
  int push_button_state = digitalRead(BUTTON);
  delay(500);
  Serial.println("previous_button_state is " + String(previous_button_state));
  if (push_button_state == HIGH) {
    if (previous_button_state == LOW) {
      sendButtonPushedMessage();
      delay(500);
      previous_button_state = HIGH;
      Serial.println("Changing previous_button_state from LOW to HIGH");
    }
  } else {
    if (previous_button_state == HIGH) {
      previous_button_state = LOW;
      Serial.println("Changing previous_button_state from HIGH to LOW");
    }
  }

  int ADC = analogRead(FLEX);
  delay(500);
  Serial.println("ADC is " + String(ADC));
  Serial.println("previous_flex_state is " + String(previous_flex_state));
  // float V_flex = ADC * VCC / 1023.0;
  // float R_flex = R_DIV * (VCC / V_flex - 1.0);
  // float R_flex = (1023.0 - ADC) / (ADC * R_DIV);
  // Serial.println("V_flex is " + String(V_flex));
  // Serial.println("Flex sensor resistance is " + String(R_flex) + " ohms");

  // float angle = map(R_flex, R_FLAT, R_BENT, 0, 90.0);
  // Serial.println("Flex sensor bent angle is " + String(angle) + " degrees");
  if (ADC >= 1500) {
    if (previous_flex_state == LOW) {
      previous_flex_state = HIGH;
      Serial.println("Changing previous_flex_state from LOW to HIGH");
    }
  } else {
    if (previous_flex_state == HIGH) {
      sendFlexSensorMessage();
      delay(500);
      previous_flex_state = LOW;
      Serial.println("Changing previous_flex_state from HIGH to LOW");
    }
  }

  // delay(2000);
}
