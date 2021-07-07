#include "Arduino.h"
#include <ESP32AnalogRead.h>
#ifdef V_REF  //if the macro MEDIAN_MAX_SIZE is defined 
#undef V_REF  //un-define it
#define V_REF  1200//redefine it with the new value
#endif 
ESP32AnalogRead adc;
void setup()
{
	adc.attach(32);
	Serial.begin(115200);
}

void loop()
{
	delay(50);
	Serial.println("Voltage = "+String(adc.readVoltage()));
}
