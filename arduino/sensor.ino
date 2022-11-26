#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

int inputPin[] = {4,2,27,32};

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
    pinMode(inputPin[i], INPUT);
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
  bool sensor[4];
  // connect endpoint
  HTTPClient http;
  http.begin(endPoint);
  http.addHeader("Content-Type", "application/json");
  
  // Arduino JSON 
  DynamicJsonDocument data(1024);
  
  // trigger 발생
  for (int i = 0; i < 4; i++){
    sensor[i] = digitalRead(inputPin[i]); 
  }

  // print distancce
  for (int i = 0; i < 4; i++){
    Serial.print("sensor " + i + " : " + sensor[i] + "\n");
  }
  
  // JSON Object
  for (int i = 0; i < 4; i++){
    data["sensor" + String(i)] = sensor[i];
  }
  
  String requestBody;
  serializeJson(data, requestBody);
  Serial.print(requestBody);
  int httpCode = http.POST(requestBody);
  Serial.print(httpCode);
  http.end();
  
  delay(300);
}
