#include <WiFi.h>
#include <FirebaseESP32.h>
#include <MQUnifiedsensor.h>

// Firebase configuration
#define FIREBASE_HOST "safezone-8496c.firebaseio.com"
#define FIREBASE_AUTH "AIzaSyATnRiTlsK0DbEpymmBwG0YCULvwYKJ4ho"

// WiFi credentials
#define WIFI_SSID "your-SSID"
#define WIFI_PASSWORD "your-password"

#define placa "ESP-32"
#define Voltage_Resolution 3.3
#define pin 4
#define type "MQ-135"
#define ADC_Bit_Resolution 12
#define RatioMQ135CleanAir 3.6
MQUnifiedsensor MQ135(placa, Voltage_Resolution, ADC_Bit_Resolution, pin, type);

// MQ-3 setup
const int analogPin = 36;

char jenisgas[6][10] = {"CO","Alcohol","CO2","Tolueno","NH4","Aceton"};
float gasA[6] = {605.18, 77.255, 110.47, 44.947, 102.2, 34.668};
float gasB[6] = {-3.937, -3.18, -2.862, -3.445, -2.473};
int itemcheck = 2;

// Firebase objects
FirebaseData firebaseData;
FirebaseJson json;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  // MQ-135 initialization and calibration
  MQ135.setRegressionMethod(1);
  MQ135.setA(gasA[itemcheck]);
  MQ135.setB(gasB[itemcheck]);
  MQ135.init();

  Serial.print("Calibrating please wait.");
  float calcR0 = 0;
  for (int i = 1; i <= 10; i++) {
    MQ135.update();
    calcR0 += MQ135.calibrate(RatioMQ135CleanAir);
    Serial.print(".");
  }
  MQ135.setR0(calcR0 / 10);
  Serial.println("  done!");

  if (isinf(calcR0)) {
    Serial.println("Warning: Connection issue detected, R0 is infinite (Open circuit detected). Please check your wiring and supply.");
    while (1);
  }
  if (calcR0 == 0) {
    Serial.println("Warning: Connection issue detected, R0 is zero (Analog pin with short circuit to ground). Please check your wiring and supply.");
    while (1);
  }

  MQ135.serialDebug(false);
  delay(1000);
}

void loop() {
  MQ135.update();
  int sensorValue = analogRead(analogPin);
  float hasil = MQ135.readSensor();
  
  // Print sensor values
  Serial.print("Nilai Sensor MQ-3: ");
  Serial.println(sensorValue);
  Serial.print(jenisgas[itemcheck]);
  Serial.print(" : ");
  Serial.print(hasil);
  Serial.println(" PPM");

  // Create JSON object
  json.set("/MQ3", sensorValue);
  json.set("/MQ135", hasil);

  // Send JSON data to Firebase
  if (Firebase.pushJSON(firebaseData, "/sensorData", json)) {
    Serial.println("Data sent to Firebase");
  } else {
    Serial.println("Failed to send data to Firebase");
    Serial.println(firebaseData.errorReason());
  }

  delay(1000);
}
