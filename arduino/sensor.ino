#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

int echoPin0 = 4;
int triggerPin0 = 0;
int echoPin1 = 2;
int triggerPin1 = 15;
int echoPin2 = 27;
int triggerPin2 = 14;
int echoPin3 = 32;
int triggerPin3 = 33;

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
  
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(triggerPin0, OUTPUT);
  pinMode(triggerPin1, OUTPUT);
  pinMode(triggerPin2, OUTPUT);
  pinMode(triggerPin3, OUTPUT);
  pinMode(echoPin0, INPUT);
  pinMode(echoPin1, INPUT);
  pinMode(echoPin2, INPUT);
  pinMode(echoPin3, INPUT);
  
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
  long duration0, distance0, duration1, distance1, duration2, distance2, duration3, distance3;

  // connect endpoint
  HTTPClient http;
  http.begin(endPoint);
  http.addHeader("Content-Type", "application/json");
  
  // Arduino JSON 
  DynamicJsonDocument data(1024);
  // trigger 발생
  digitalWrite(triggerPin0, LOW);
  delay(2);
  digitalWrite(triggerPin0, HIGH);
  delay(10);
  digitalWrite(triggerPin0, LOW);
  duration0 = pulseIn(echoPin0, HIGH);
  
  digitalWrite(triggerPin1, LOW);
  delay(2);
  digitalWrite(triggerPin1, HIGH);
  delay(10);
  digitalWrite(triggerPin1, LOW);
  duration1 = pulseIn(echoPin1, HIGH);

  digitalWrite(triggerPin2, LOW);
  delay(2);
  digitalWrite(triggerPin2, HIGH);
  delay(10);
  digitalWrite(triggerPin2, LOW);
  duration2 = pulseIn(echoPin2, HIGH);

  digitalWrite(triggerPin3, LOW);
  delay(2);
  digitalWrite(triggerPin3, HIGH);
  delay(10);
  digitalWrite(triggerPin3, LOW);
  duration3 = pulseIn(echoPin3, HIGH);
  
  // echo 입력
  // duration0 = pulseIn(echoPin0, HIGH);
  // duration1 = pulseIn(echoPin1, HIGH);
  // duration2 = pulseIn(echoPin2, HIGH);
  // duration3 = pulseIn(echoPin3, HIGH);
  distance0 = duration0 * 17 / 1000;
  distance1 = duration1 * 17 / 1000;
  distance2 = duration2 * 17 / 1000;
  distance3 = duration3 * 17 / 1000;
  
  Serial.print("\nDistance0 : ");
  Serial.print(distance0);
  Serial.print("cm ");
  
  Serial.print("Duration0 : ");
  Serial.print(duration0);
  
  Serial.print("\nDistance1 : ");
  Serial.print(distance1);
  Serial.print("cm ");
  
  Serial.print("Duration1 : ");
  Serial.print(duration1);
  Serial.print("\n");

  Serial.print("\nDistance2 : ");
  Serial.print(distance2);
  Serial.print("cm ");
  
  Serial.print("Duration2 : ");
  Serial.print(duration2);

  Serial.print("\nDistance3 : ");
  Serial.print(distance3);
  Serial.print("cm ");
  
  Serial.print("Duration3 : ");
  Serial.print(duration3);
  // JSON Object
  data["distance0"] = distance0;
  data["distance1"] = distance1;
  data["distance2"] = distance2;
  data["distance3"] = distance3;

  String requestBody;
  serializeJson(data, requestBody);
  Serial.print(requestBody);
  int httpCode = http.POST(requestBody);
  Serial.print(httpCode);
  http.end();
  
  delay(300);
}
