#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

int echoPin0 = 4;
int triggerPin0 = 0;
int echoPin1 = 2;
int triggerPin1 = 15;


// WiFi 연결 
const char* ssid = "chanosong";
const char* pw = "cksgh206";

// Server domain
String endPoint = "http://14.52.69.42:5000/sensor";

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
  pinMode(echoPin0, INPUT);
  pinMode(echoPin1, INPUT);

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
  long duration0, distance0, duration1, distance1;

  // connect endpoint
  HTTPClient http;
  http.begin(endPoint);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  
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
  
  // echo 입력
  // duration0 = pulseIn(echoPin0, HIGH);
  // duration1 = pulseIn(echoPin1, HIGH);
  distance0 = duration0 * 17 / 1000;
  distance1 = duration1 * 17 / 1000;
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

  // JSON Object
  data["distance0"] = distance0;
  data["distance1"] = distance1;

  String sData;
  serializeJson(data, sData);
  Serial.print(sData);
  int httpCode = http.POST(sData);
  Serial.print(httpCode);
  http.end();
  
  delay(300);
}
