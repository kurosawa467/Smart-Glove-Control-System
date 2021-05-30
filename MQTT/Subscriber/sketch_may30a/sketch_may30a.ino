#include "PubSubClient.h"
#include "ESP8266WiFi.h"

#define MSG_BUFFER_SIZE (50)

const char* ssid = "WG01";
const char* wifi_password = "321losgehts";

const char* mqtt_server = "192.168.178.100";
const char* button_topic = "/esp8266/button";
const char* flex_topic = "/esp8266/flex";
const char* mqtt_username = "mosquitto";
const char* mqtt_password = "mosquitto";
const char* clientID = "ESP8266";

const int BLINK_SHORT = 2;
const int BLINK_MID = 5;
const int BLINK_LONG = 8;

WiFiClient espClient;
PubSubClient client(mqtt_server, 1883, espClient);
unsigned long lastMessage = 0;
char message[MSG_BUFFER_SIZE];
int value = 0;
const int LED_Pin = 5;

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
  
  if ((char)payload[0] == '0') {
    LED_blink(BLINK_LONG);
  } else if ((char)payload[0] == '1') {
    LED_blink(BLINK_MID);
  } else {
    LED_blink(BLINK_SHORT);
  }
}

void LED_blink(int blinkTime) {
  int counter = 0;
  while (counter <= blinkTime) {
    digitalWrite(BUILTIN_LED, LOW);
    digitalWrite(LED_Pin, HIGH);
    delay(1000);
    digitalWrite(BUILTIN_LED, HIGH);
    digitalWrite(LED_Pin, LOW);
    delay(1000);
    counter++;
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(LED_Pin, OUTPUT);
  digitalWrite(BUILTIN_LED, HIGH);
  digitalWrite(LED_Pin, LOW);
  LED_blink(BLINK_SHORT);
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
