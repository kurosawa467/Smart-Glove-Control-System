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
const char* clientID = "ESP8266/1";

const int RED_ANALOG_PIN = 14;
const int GREEN_ANALOG_PIN = 12;
const int BLUE_ANALOG_PIN = 15;
const int RED_DIGITAL_PIN = 5;
const int GREEN_DIGITAL_PIN = 4;
const int BLUE_DIGITAL_PIN = 0;

int analogLedColor = 7;
int analogLedBrightness = 100;
int digitalLedColor = 7;
int digitalLedBrightness = 100;

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

  int command = payload[0] - 48;

  int color = 7;
  int brightness = 100;
  if(!strcmp(topic, analog_led_topic)){
    color = analogLedColor;
    brightness = analogLedBrightness;
  } else {
    color = digitalLedColor;
    brightness = digitalLedBrightness;
  }

  //if is the case an LED has to be set new from the beginning
  if(true){
    switch(command){
      case 1:
        color = (color+1)%8;
        break;
      case 2:
        color =  color==0? 7 : color-1;
        break;
      case 3:
        brightness = brightness < 10? 0 : brightness-10;
        break;
      case 4:
        brightness = brightness > 90? 100 : brightness+10;        
        break;
      default:
        Serial.println("Error wrong wrong command!!");
    }
  } else { //this case is the case where we change the the LED value based on their last state
    // color is a 3-bit number decoding rgb
      color = payload[0] - 48 ;
      
      brightness = 0;
      for (int i = 2; i < length; i++)
      {
        brightness = brightness * 10 + payload[i] - 48;
      }
  }
  if(!strcmp(topic, analog_led_topic)){
    analogLedColor = color;
    analogLedBrightness = brightness;
  } else {
    digitalLedColor = color;
    digitalLedBrightness = brightness;
  }
  setLED(color,brightness,topic);

  //get Command id
  int id = 0;
  for (int i = 2; i < length; i++)
      {
        id = id * 10 + payload[i] - 48;
      }
  Serial.print("Command ID:");
  Serial.println(id);
}

void setLED(int color, int brightness, char* topic){
  Serial.print("Color:");
  Serial.println(color);

  int green = color % 2;
  color = color >> 1;
  int blue = color % 2;
  color = color >> 1;
  int red = color % 2;

  Serial.print("Brightness:");
  Serial.println(brightness);
  
  if(!strcmp(topic, analog_led_topic)){  
    set_analog_led( red, green, blue, brightness);
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
  digitalWrite(RED_DIGITAL_PIN, (red+1)%2);
  digitalWrite(GREEN_DIGITAL_PIN, (green+1)%2);
  digitalWrite(BLUE_DIGITAL_PIN, (blue+1)%2);
}

char** splitStr( String str, char c){
  char** input =0;
  return input;
}


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
}
