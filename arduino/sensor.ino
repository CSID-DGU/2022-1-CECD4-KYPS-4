#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

int echoPin[] = {4,2,27,32};
int triggerPin[] = {0,15,14,33};

// WiFi 연결 
const char* ssid = "HCN-413";
const char* pw = "18778000";

// Server domain
String endPoint = "http://192.168.0.7:5000/sensor";
  
// JSONBuffer
// StaticJsonDocument<200> jsonBuffer;

WiFiServer server(80);

// vcc leftmost below
// gnd rightmost upper
// echo GPIO 4
// trigger GPIO 4
void setup() {
  
  // Pin initialize
  Serial.begin(115200);
  for (int i = 0; i < 4; i++) {
    pinMode(triggerPin[i], OUTPUT);
    pinMode(echoPin[i], INPUT);
  }
  
  Serial.print("Connecting to ");
  Serial.print(ssid);

  WiFi.begin(ssid, pw);
  
  while(WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }

  Serial.print("\nWiFi Connected.");
  Serial.print("IP Address : ");
  Serial.print(WiFi.localIP());

  server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  // long duration0, distance0, duration1, distance1, duration2, distance2, duration3, distance3;
  long duration[4];
  long distance[4];
  // connect endpoint
  HTTPClient http;
  http.begin(endPoint);
  http.addHeader("Content-Type", "application/json");
  
  // Arduino JSON 
  DynamicJsonDocument data(1024);
  
  // trigger 발생
  for (int i = 0; i < 4; i++){
    digitalWrite(triggerPin[i], LOW);
    delayMicroseconds(2);
    digitalWrite(triggerPin[i], HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin[i], LOW);
    duration[i] = pulseIn(echoPin[i], HIGH); 
  }
    
  // Get distance
  for (int i = 0; i < 4; i++){
    distance[i] = duration[i] * 17 / 1000;
  }

  // print distancce
  for (int i = 0; i < 4; i++){
    Serial.print("Distance" + String(i) + ": ");
    Serial.print(distance[i]);
    Serial.print("cm ");  
    Serial.print("Duration" + String(i) + ": ");
    Serial.print(duration[i]);
    Serial.print("ms\n");
  }
  
  // JSON Object
  for (int i = 0; i < 4; i++){
    data["distance" + String(i)] = distance[i];
  }
  
  String requestBody;
  serializeJson(data, requestBody);
  Serial.print(requestBody);
  int httpCode = http.POST(requestBody);
  Serial.print(httpCode);
  http.end();
  
  delay(300);
}
