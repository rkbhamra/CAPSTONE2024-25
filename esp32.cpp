#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "ESP32-AP";
const char* password = "123456789";
const char* pythonServerIP = "123.456.789.0";

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);

  WiFi.softAP(ssid, password);

  Serial.println("Access Point Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/test_post", HTTP_POST, [](AsyncWebServerRequest *request){
    String image_data = request->arg("image");

    HTTPClient http;
    String serverURL = "http://" + String(pythonServerIP) + ":5000/test_post";
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String json_payload = "{\"image\": \"" + image_data + "\"}";

    int httpCode = http.POST(json_payload);

    if (httpCode > 0) {
      String payload = http.getString();
      request->send(200, "application/json", payload);
    } else {
      request->send(500, "application/json", "{\"message\": \"Error sending request\"}");
    }
    http.end();
  });

  server.begin();
}

// need this leave empty
void loop() {}
