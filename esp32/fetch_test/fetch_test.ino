// Step 5 test: connect to Wi-Fi, fetch a public HTTPS JSON API,
// parse it with ArduinoJson and print fields to Serial (115200 baud).
// The Spotify version will follow the same fetch -> parse -> print pattern.

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "secrets.h"   // WIFI_SSID / WIFI_PASSWORD - copy secrets.example.h

const unsigned long WIFI_TIMEOUT_MS = 20000;

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Give up after 20 s instead of looping forever on a wrong password / 5 GHz network
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - start > WIFI_TIMEOUT_MS) {
      Serial.println("\nWi-Fi connect timed out - check SSID/password (2.4 GHz only)");
      return;
    }
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());

  fetchData();
}

void loop() {
}

void fetchData() {
  HTTPClient http;
  http.begin("https://api.github.com/users/octocat");

  int httpCode = http.GET();
  Serial.print("Status code: ");
  Serial.println(httpCode);

  if (httpCode == 200) {
    String payload = http.getString();

    JsonDocument doc;
    DeserializationError err = deserializeJson(doc, payload);
    if (err) {
      Serial.print("JSON parse failed: ");
      Serial.println(err.c_str());
      http.end();
      return;
    }

    String name = doc["name"] | "(none)";
    String company = doc["company"] | "(none)";
    int repos = doc["public_repos"] | 0;

    Serial.println("--- Parsed ---");
    Serial.println("Name: " + name);
    Serial.println("Company: " + company);
    Serial.print("Public repos: ");
    Serial.println(repos);
  } else {
    Serial.println("Request failed: " + http.errorToString(httpCode));
  }

  http.end();
}
