#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>

// serverURL: http://<ESP32_IP>/test_post
const char* ssid = "";
const char* password = "";

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    Serial.println(WiFi.localIP()); // ESP32_IP
  }

  Serial.println("Connected to WiFi!");

  server.on("/test_post", HTTP_POST, [](AsyncWebServerRequest *request){
    String image_data = request->arg("image");

    HTTPClient http;
    http.begin("http://<Python_Server_IP>:5000/test_post");
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

void loop() { }