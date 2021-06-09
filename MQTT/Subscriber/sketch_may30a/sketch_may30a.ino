#include "PubSubClient.h"
#include "ESP8266WiFi.h"
#include "WifiAccess.h"

#define MSG_BUFFER_SIZE (50)

const char* ssid = ssid_name;
const char* wifi_password = password_name;

const char* mqtt_server = server_ip;
const char* button_topic = "/esp8266/button";
const char* flex_topic = "/esp8266/flex";
const char* mqtt_username = "mosquitto";
const char* mqtt_password = "mosquitto";
const char* clientID = "ESP8266";


WiFiClient espClient;
PubSubClient client(mqtt_server, 1883, espClient);
unsigned long lastMessage = 0;
char message[MSG_BUFFER_SIZE];
int value = 0;
const int RED_Pin = 14;
const int GREEN_Pin = 12;
const int BLUE_Pin = 15;

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
    client.subscribe(button_topic);
    client.subscribe(flex_topic);
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
  
  int ratio = 0;
  for(int i=2;i<length;i++)
  {
    ratio = ratio*10 + payload[i] - 48;
  }
  Serial.print("Ratio:");
  Serial.println(ratio);

  set_led(color,ratio);
  
}

void set_led(int color, int ratio){
  int green = color%2;
  color = color>>1;
  int blue = color%2;
  color = color>>1;
  int red = color%2;
  
  int pwmIntervals = 100;

  int stepSize = (pwmIntervals * log10(2))/(log10(255));

  int brightness = pow (2, (ratio / stepSize)) - 1;

  Serial.print("Brightness:");
  Serial.println(brightness);

  analogWrite(RED_Pin, red * brightness);
  analogWrite(GREEN_Pin, green * brightness);
  analogWrite(BLUE_Pin, blue * brightness);
  
}

void dim(){
  int pwmIntervals = 100;
  int del = 5;

  int R = (pwmIntervals * log10(2))/(log10(255));
  while(true){
    int brightness = 0;
    for(int interval=0; interval<= pwmIntervals; interval++){
      brightness = pow (2, (interval / R)) - 1;
      analogWrite(RED_Pin, brightness);
      delay(del);
    }
    for(int interval= pwmIntervals; interval>=0; interval--){
      brightness = pow (2, (interval / R)) - 1;
      analogWrite(RED_Pin, brightness);
      delay(del);
    }
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(RED_Pin, OUTPUT);
  pinMode(GREEN_Pin, OUTPUT);
  pinMode(BLUE_Pin, OUTPUT);
  digitalWrite(RED_Pin, LOW);
  digitalWrite(GREEN_Pin, LOW);
  digitalWrite(BLUE_Pin, LOW);
  connect_WiFi();
  connect_MQTT();
  client.setCallback(callback);
}

void loop() {
  Serial.setTimeout(5000*60);
  if (!client.connected()) {
    connect_MQTT();
  }
  client.loop();
  // delay(2000);
}
