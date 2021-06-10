#include "PubSubClient.h"
#include "ESP8266WiFi.h"
#include "WifiAccess.h"

#define MSG_BUFFER_SIZE (50)

const char* ssid = ssid_name;
const char* wifi_password = password_name;

const char* mqtt_server = server_ip;
const char* analog_led_topic = "/esp8266/1.1";
const char* digital_led_topic = "/esp8266/1.2";
const char* mqtt_username = "mosquitto";
const char* mqtt_password = "mosquitto";
const char* clientID = "ESP8266";

const int RED_ANALOG_PIN = 14;
const int GREEN_ANALOG_PIN = 12;
const int BLUE_ANALOG_PIN = 15;
const int RED_DIGITAL_PIN = 10;
const int GREEN_DIGITAL_PIN = 9;
const int BLUE_DIGITAL_PIN = 8;

WiFiClient espClient;
PubSubClient client(mqtt_server, 1883, espClient);
unsigned long lastMessage = 0;
char message[MSG_BUFFER_SIZE];
int value = 0;

void connect_WiFi() {
  Serial.print("ESP8266 is trying connect to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
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
    client.subscribe(analog_led_topic);
    client.subscribe(digital_led_topic);
    Serial.println("Connected to MQTT broker");
  } else {
    Serial.println("Connection failed");
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived. Topic: ");
  Serial.print(topic);
  Serial.print(". ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println(".");

  
  // color is a 3-bit number decoding rgb
  int color = payload[0] - 48 ;
  Serial.print("Color:");
  Serial.println(color);

  int green = color % 2;
  color = color >> 1;
  int blue = color % 2;
  color = color >> 1;
  int red = color % 2;

  if(strcmp(topic, analog_led_topic)){

    int ratio = 0;
    for (int i = 2; i < length; i++)
    {
      ratio = ratio * 10 + payload[i] - 48;
    }
    Serial.print("Ratio:");
    Serial.println(ratio);
  
    set_analog_led( red, green, blue, ratio);
  } else {
    set_digital_led(red, green, blue);
  }

}

void set_analog_led(int red, int green, int blue, int ratio) {

  int pwmIntervals = 100;

  int stepSize = (pwmIntervals * log10(2)) / (log10(255));

  int brightness = pow (2, (ratio / stepSize)) - 1;

  Serial.print("Brightness:");
  Serial.println(brightness);

  analogWrite(RED_ANALOG_PIN, red * brightness);
  analogWrite(GREEN_ANALOG_PIN, green * brightness);
  analogWrite(BLUE_ANALOG_PIN, blue * brightness);

}
void set_digital_led(int red, int green, int blue){
  digitalWrite(RED_DIGITAL_PIN, red);
  digitalWrite(GREEN_DIGITAL_PIN, green);
  digitalWrite(BLUE_DIGITAL_PIN, blue);
}

/*void dim() {
  int pwmIntervals = 100;
  int del = 5;

  int R = (pwmIntervals * log10(2)) / (log10(255));
  while (true) {
    int brightness = 0;
    for (int interval = 0; interval <= pwmIntervals; interval++) {
      brightness = pow (2, (interval / R)) - 1;
      analogWrite(RED_Pin, brightness);
      delay(del);
    }
    for (int interval = pwmIntervals; interval >= 0; interval--) {
      brightness = pow (2, (interval / R)) - 1;
      analogWrite(RED_Pin, brightness);
      delay(del);
    }
  }
}*/

void setup() {
  Serial.begin(9600);
  pinMode(RED_ANALOG_PIN, OUTPUT);
  pinMode(GREEN_ANALOG_PIN, OUTPUT);
  pinMode(BLUE_ANALOG_PIN, OUTPUT);
  digitalWrite(RED_ANALOG_PIN, LOW);
  digitalWrite(GREEN_ANALOG_PIN, LOW);
  digitalWrite(BLUE_ANALOG_PIN, LOW);

  pinMode(RED_DIGITAL_PIN, OUTPUT);
  pinMode(GREEN_DIGITAL_PIN, OUTPUT);
  pinMode(BLUE_DIGITAL_PIN, OUTPUT);
  digitalWrite(RED_DIGITAL_PIN, LOW);
  digitalWrite(GREEN_DIGITAL_PIN, LOW);
  digitalWrite(BLUE_DIGITAL_PIN, LOW);
  connect_WiFi();
  connect_MQTT();
  client.setCallback(callback);
}

void loop() {
  Serial.setTimeout(5000 * 60);
  if (!client.connected()) {
    connect_MQTT();
  }
  client.loop();
  // delay(2000);
}
