#include "PubSubClient.h"
#include "WiFi.h"

const char* ssid = "4025 mk2";
const char* wifi_password = "147258369a";

const char* mqtt_server = "192.168.0.12";
const char* button_topic = "/esp32/button";
const char* flex_topic = "/esp32/flex";
const char* mqtt_username = "mosquitto";
const char* mqtt_password = "mosquitto";
const char* clientID = "ESP32";

const int BUTTON = 32;
const int FLEX = 33;
int previous_button_state = LOW;
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


/*void setup() {
  connect_WiFi();
  connect_MQTT();
}
*/