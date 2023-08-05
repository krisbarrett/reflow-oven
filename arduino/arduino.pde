#include "max6675.h"

// pins
int zeroCross = 2;
int led = 4;
int relayLed = 5;
int thermoGND = 8;
int thermoVCC = 9;
int thermoDO = 10;
int thermoCS = 11;
int thermoCLK = 12;
int heater = 13;

// state information
boolean running = true;
int wasHigh = 1;
double lastTemp = 0;
int lastTempMs = 0;
int heaterState = LOW;
int ledState = LOW;
bool testMode = false;

// command buffer
String cmdBuffer = "";

// parameters
float temp = 36;
float hystHigh = 1;
float hystLow = 1;

// initialize thermocouple
MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);
  
void toggleLed() {
  if(ledState == LOW) {
    digitalWrite(led, HIGH);
    ledState = HIGH;
  }
  else {
    digitalWrite(led, LOW);
    ledState = LOW;
  }
}

void processCmd() {
  String cmd = "";
  String arg = "";
  
  cmdBuffer = cmdBuffer.trim();
  int index = cmdBuffer.indexOf(' ');
  if(index != -1) {
    cmd = cmdBuffer.substring(0, index);
    arg = cmdBuffer.substring(index+1);
  }
  else {
    cmd = cmdBuffer;
  }
  
  if(cmd.equals("temp")) {
    if(testMode) {
      Serial.println(temp);
    } else {
      Serial.println(thermocouple.readCelsius());
    }
  } else if(cmd.equals("start")) {
    running = true;
    Serial.println("ack");
  }
  else if(cmd.equals("halt")) {
    running = false;
    Serial.println("ack");
  }
  else if(cmd.equals("set_temp")) {
    temp = stof(arg);
    if(testMode) {
      Serial.println(temp);
    } else {
      Serial.println(thermocouple.readCelsius());
    }
  }
  else if(cmd.equals("set_hyst_high")) {
    hystHigh = stof(arg);
    Serial.println("ack");
  }
  else if(cmd.equals("set_hyst_low")) {
    hystLow = stof(arg);
    Serial.println("ack");
  }
  else if(cmd.equals("get_temp")) {
    Serial.println(temp);
  }
  else if(cmd.equals("get_hyst_high")) {
    Serial.println(hystHigh);
  }
  else if(cmd.equals("get_hyst_low")) {
    Serial.println(hystLow);
  }
  else {
    Serial.println("err");
  }
}

// read freqnuency is limited by converstion rate of MAX6675
double cmdTemp() {
  int time = millis();
  if(time >= lastTempMs + 220) {
    lastTempMs = time;
    lastTemp = thermocouple.readCelsius();
  }
  return lastTemp;
}

// converts a string to a float
float stof(String s) {
  char str[128];
  s.toCharArray(str,128);
  return atof(str);
}

void nextState() {
  digitalWrite(heater, heaterState);
  digitalWrite(relayLed, heaterState);
  double currentTemp = cmdTemp();
  if(heaterState == HIGH) {
    heaterState = (currentTemp >= temp) ? LOW : HIGH;
  }
  else if(heaterState == LOW){
    heaterState = (currentTemp <= temp) ? HIGH : LOW;
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(thermoVCC, OUTPUT); digitalWrite(thermoVCC, HIGH);
  pinMode(thermoGND, OUTPUT); digitalWrite(thermoGND, LOW);
  pinMode(led, OUTPUT); digitalWrite(led, LOW);
  pinMode(heater, OUTPUT); digitalWrite(heater, LOW);
  pinMode(relayLed, OUTPUT); digitalWrite(relayLed, LOW);
  pinMode(zeroCross, INPUT);
  
  // wait for MAX chip to stabilize
  delay(500);
}

void loop() {
   if(Serial.available()) {
     while(Serial.available()) {
       char c = Serial.read();
       if(c == '\n') {
         processCmd();
         cmdBuffer = "";
       }
       else {
         cmdBuffer += c;
       }
     }
   }
   if(digitalRead(zeroCross) == LOW) {
     // determine next state on zero crossing
     if(wasHigh) {
       toggleLed();
       if(running) {
         nextState();
       }
       else {
         digitalWrite(heater, LOW);
         digitalWrite(relayLed, LOW);
       }
       wasHigh = 0;
     }
   } else {
     wasHigh = 1;
   }
}
