#include <WiFi.h>
#include <WiFiUdp.h>
/*Button Configuration*/
const int button = 27;
uint8_t val_old = 0;

/* WiFi network name and password */
const char * ssid = "***";
const char * pwd = "****";

// IP address to send UDP data to.
// it can be ip address of the server or
// a network broadcast address
// here is broadcast address
const char * udpAddress = "****";
const int udpPort = 44444;

//create UDP instance
WiFiUDP udp;

void setup() {
  Serial.begin(115200);

  //configure GPIO pin
  pinMode(button, INPUT_PULLUP); // pull up HIGH when button not pressed

  //Connect to the WiFi network
  WiFi.begin(ssid, pwd);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  //This initializes udp and transfer buffer
  udp.begin(udpPort);
}

void loop() {

  //get button state
   uint8_t val = digitalRead(button); // perform digital reading

  if( val != val_old) {
      val_old = val;
      //data will be sent to server
      uint8_t buffer[50] = "";
      uint8_t message_length = 0;
    
      //write state in 
      if (val == 0) { // becomes LOW when button is pressed
       memcpy(buffer, "yes", 3); // set buffer to yes
       message_length = 3;
      }
      else {
        memcpy(buffer, "no", 2); // set buffer to yes
        message_length = 2;
      }
      
      //send data to server;
      udp.beginPacket(udpAddress, udpPort);
      udp.write(buffer, message_length);
      udp.endPacket();
      memset(buffer, 0, 50);
      
      //processing incoming packet, must be called before reading the buffer
      udp.parsePacket();
      //receive response from server
      if (udp.read(buffer, 50) > 0) {
        Serial.print("Server to client: ");
        Serial.println((char *)buffer);
      }
  }
  //Wait for 1 second
  delay(100);
}
