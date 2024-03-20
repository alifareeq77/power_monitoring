#include "ACS712.h"
#include <ZMPT101B.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> // Include the ArduinoJson library

// Define ACS712 and ZMPT101B objects
ACS712 ACS(36, 3.3, 4095, 66);
ZMPT101B voltageSensor(39, 50.0);

// Define WiFi credentials
// const char* ssid = "ali fareeq";
// const char* password = "11qq22www";
// home network
const char* ssid = "Oops_404 !";
const char* password = "new_password";


// Define Django backend server address and endpoint URL
const char* serverAddress = "http://192.168.0.115:8000/esp32/receive/87bc5cfd-e87d-424c-9b7c-01e5b93119d1/";


// Initialize HTTPClient object
HTTPClient http;

// Previous sensor readings
float prevCurrent = 0;
float prevVoltage = 0;
const int relay = 22;

bool get_switch_status() {
  http.begin(serverAddress); // Replace "/endpoint/" with your actual endpoint
  int httpResponseCode = http.GET();

  // Check for successful response
  if (httpResponseCode == HTTP_CODE_OK) {
    String response = http.getString();
    // Parse JSON response to get is_switched value
    DynamicJsonDocument jsonDoc(1024);
    deserializeJson(jsonDoc, response);
    // Extract is_switched value and return it
    bool is_switched = jsonDoc["is_switched"];
    return is_switched;
  }
  http.end();  
  // Return false if there's any error
  return false;
}

// Function to send sensor data to the endpoint
void postDataToEndpoint(float voltage, float current) {
  // Construct JSON data
  String json_data = "{\"voltage\": " + String(voltage) + ", \"current\": " + String(current) + "}";

  // Begin HTTP request
  http.begin(serverAddress);
  http.addHeader("Content-Type", "application/json");

  // Send POST request with JSON data
  int httpResponseCode = http.POST(json_data);

  // Check for successful response
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println(httpResponseCode);
    Serial.println(response);
  } else {
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
  }

  // End HTTP request
  http.end();
}



void setup() {
  Serial.begin(115200);
  voltageSensor.setSensitivity(850.5f);
  pinMode(2,OUTPUT);
  pinMode(relay, OUTPUT);
  // Connect to WiFi
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  digitalWrite(2,HIGH);
}


void loop() {
    bool switch_status= get_switch_status();
    if(switch_status){
      digitalWrite(relay, HIGH);
      Serial.println("Current Flowing");
      }
    else{
        digitalWrite(relay, LOW);
        Serial.println("Current Not Flowing");
      }
          
  
  // Read current from ACS712 sensor
  float average = 0;
  for (int i = 0; i < 100; i++) {
    average += ACS.mA_AC();
  }
  float mA = average / 100.0;
  Serial.println(mA);
  // Read voltage from ZMPT101B sensor
  float voltage = voltageSensor.getRmsVoltage(5);

  // Filter out noise and adjust values
  if (mA < 200) {
    mA = 0;
  }
  if (voltage < 80) {
    voltage = 0;
  }

  // Check if current or voltage has changed significantly
  if (abs(mA - prevCurrent) >= 200 || abs(voltage - prevVoltage) >= 10) {
    // Send sensor data to the endpoint
    postDataToEndpoint(voltage, mA);

    // Update previous readings
    prevCurrent = mA;
    prevVoltage = voltage;
  }

 

  // Delay before next iteration
    delay(1000);
}
