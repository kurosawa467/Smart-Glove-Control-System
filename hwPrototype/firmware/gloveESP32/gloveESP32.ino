#include <ESP32AnalogRead.h>
//#include "connectivity.c"

////////
///////////////////////////////////////////////
#include <Arduino.h>
#include <Adafruit_BNO08x.h>
#define BNO08X_RESET -1

struct euler_t {
  float yaw;
  float pitch;
  float roll;
} ypr;

Adafruit_BNO08x  bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

sh2_SensorId_t reportType = SH2_ARVR_STABILIZED_RV;
long reportIntervalUs = 5000;

void setReports(sh2_SensorId_t reportType, long report_interval) {
  Serial.println("Setting desired reports");
  if (! bno08x.enableReport(reportType, report_interval)) {
    Serial.println("Could not enable stabilized remote vector");
  }
}

void quaternionToEuler(float qr, float qi, float qj, float qk, euler_t* ypr, bool degrees = false) {

    float sqr = sq(qr);
    float sqi = sq(qi);
    float sqj = sq(qj);
    float sqk = sq(qk);

    ypr->yaw = atan2(2.0 * (qi * qj + qk * qr), (sqi - sqj - sqk + sqr));
    ypr->pitch = asin(-2.0 * (qi * qk - qj * qr) / (sqi + sqj + sqk + sqr));
    ypr->roll = atan2(2.0 * (qj * qk + qi * qr), (-sqi - sqj + sqk + sqr));

    if (degrees) {
      ypr->yaw *= RAD_TO_DEG;
      ypr->pitch *= RAD_TO_DEG;
      ypr->roll *= RAD_TO_DEG;
    }
}

void quaternionToEulerRV(sh2_RotationVectorWAcc_t* rotational_vector, euler_t* ypr, bool degrees = false) {
    quaternionToEuler(rotational_vector->real, rotational_vector->i, rotational_vector->j, rotational_vector->k, ypr, degrees);
}

void quaternionToEulerGI(sh2_GyroIntegratedRV_t* rotational_vector, euler_t* ypr, bool degrees = false) {
    quaternionToEuler(rotational_vector->real, rotational_vector->i, rotational_vector->j, rotational_vector->k, ypr, degrees);
}
/////////////////////////////////////////////////////////
///////////////
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



ESP32AnalogRead adc;
#define ADC_BITS 12
const int FINGER_PIN_1 = 32; // Pin connected to voltage divider output

//const float ADC_SYSTEM_VCC = 5.0; // this is irrelevant of the flex sensor voltage supply
const float FLEX_VCC = 3.3;//this is the for the voltage supply of the flex sensor
const float R_DIV = 47000.0; // resistance resistor

const float STRAIGHT_RESISTANCE = 30000.0; // unfortunately not consistent between sensors. data for the one I am currently using: min 20, hand mounted typical min 22, straight 24-30
const float BEND_RESISTANCE = 50000.0; // hand mounted typical 45-50, but this one can do 100 max when bent more (not possible when hand mounted)


float getFingerAngle(){ //TODO add multi finger support
  float resistorV =adc.readVoltage(); //we can change this to adc.readMiliVolts()and modify the code a bit to have higher reading resolution, but less resolution might be better here
  float flexV=FLEX_VCC-resistorV;
  float flexR = R_DIV * (flexV/resistorV);
  float angle = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE, 0, 90.0);
  return angle;
}

void setup(){
  adc.attach(FINGER_PIN_1);
  Serial.begin(115200);
  //pinMode(FINGER_PIN_1, INPUT);
  connect_WiFi();
  connect_MQTT();

  //Serial.println("Adafruit BNO08x test!");
  if (!bno08x.begin_I2C()) {// Try to initialize!
    //Serial.println("Failed to find BNO08x chip");
    while (1) { delay(10); }
  }
  //Serial.println("BNO08x Found!");
  setReports(reportType, reportIntervalUs);
}


void sendMessage() {
  ////////////////////////////

  /////////////////////////////
  
  Serial.println("Flex sensor bending detected.");
  String fAng=String(getFingerAngle());
  String senStat = String(sensorValue.status);
  String senYaw = String(ypr.yaw);
  String senPitch = String(ypr.pitch);
  String senRoll=String(ypr.roll);
  String message = "fingerAngle:"+fAng+",imuStatus:"+senStat+",yaw:"+senYaw+",pitch:"+senPitch+",roll:"+senRoll;
  
  char* flexDetectionMessage = const_cast<char*>(message.c_str());
  if (client.publish(flex_topic, flexDetectionMessage)) {
    Serial.println("Flex detection message sent to MQTT broker");
  } else {
    Serial.println("Flex detection message failed to send to MQTT broker. Reconnecting...");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(100);
    client.publish(flex_topic, flexDetectionMessage);
  }
}


void loop(){
  ////////////IMU
  if (bno08x.wasReset()) {
    Serial.print("sensor was reset ");
    setReports(reportType, reportIntervalUs);
  }
  
  if (bno08x.getSensorEvent(&sensorValue)) {
    // in this demo only one report type will be received depending on FAST_MODE define (above)
    switch (sensorValue.sensorId) {
      case SH2_ARVR_STABILIZED_RV:
        quaternionToEulerRV(&sensorValue.un.arvrStabilizedRV, &ypr, true);
      case SH2_GYRO_INTEGRATED_RV:
        // faster (more noise?)
        quaternionToEulerGI(&sensorValue.un.gyroIntegratedRV, &ypr, true);
        break;
    }
    static long last = 0;
    long now = micros();
    //Serial.print(now - last);             Serial.print("\t");
    last = now;
    /*Serial.print(sensorValue.status);     Serial.print("\t");  // This is accuracy in the range of 0 to 3
    Serial.print(ypr.yaw);                Serial.print("\t");
    Serial.print(ypr.pitch);              Serial.print("\t");
    Serial.println(ypr.roll);*/
  }
  ////////////
  
  if (!client.connected()) {
    connect_MQTT();
  }
  client.loop();
  Serial.setTimeout(5000*60);

  sendMessage();
  
  //Serial.println("Bend: " + String(angle) + " degrees");
  //Serial.println();

  delay(500);
}
