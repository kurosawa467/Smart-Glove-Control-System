#include <ESP32AnalogRead.h>
ESP32AnalogRead adc;
#define ADC_BITS 12
const int FINGER_PIN_1 = 32; // Pin connected to voltage divider output

// Measure the voltage at 5V and the actual resistance of your
// 47k resistor, and enter them below:
const float ADC_SYSTEM_VCC = 5.0; // this is irrelevant of the flex sensor voltage supply
const float FLEX_VCC = 3.3;//this is the for the voltage supply of the flex sensor
const float R_DIV = 47000.0; // Measured resistance resistor

// Upload the code, then try to adjust these values to more
// accurately calculate bend degree.
const float STRAIGHT_RESISTANCE = 30000.0; // unfortunately not consistent between sensors. data for the one I am currently using: min 20, hand mounted typical min 22, straight 24-30
const float BEND_RESISTANCE = 50000.0; // hand mounted typical 45-50, but this one can do 100 max when bent more (not possible when hand mounted)

void setup() 
{
  adc.attach(FINGER_PIN_1);
  Serial.begin(115200);
  //pinMode(FINGER_PIN_1, INPUT);
}

void loop() 
{
  // Read the ADC, and calculate voltage and resistance from it
  //long flexADC = analogRead(FINGER_PIN_1);
  //float resistorV = (flexADC / ((1<<ADC_BITS)-1.0)) * ADC_SYSTEM_VCC ;
  float resistorV =adc.readVoltage(); //we can change this to adc.readMiliVolts()and modify the code a bit to have higher reading resolution, but less resolution might be better here
  float flexV=FLEX_VCC-resistorV;
  float flexR = R_DIV * (flexV/resistorV);
  Serial.println("Resistance: " + String(flexR) + " ohms, Rvoltage: "+String(resistorV));

  // Use the calculated resistance to estimate the sensor's
  // bend angle:
  float angle = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE,
                   0, 90.0);
  Serial.println("Bend: " + String(angle) + " degrees");
  Serial.println();

  delay(50);
}
