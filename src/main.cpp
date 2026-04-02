#include <WiFi.h>

// ⚠️ Definir credenciales antes de compilar
// Opción A: reemplazar directamente acá (no commitear)
// Opción B: crear un archivo secrets.h con las constantes y agregarlo al .gitignore
const char* ssid     = "TU_SSID";
const char* password = "TU_PASSWORD";

const int adcPin = 36;  // ADC1_CH0 (GPIO36 seguro para WiFi)
WiFiServer server(1234);

void setup() {
  Serial.begin(115200);
  delay(500);
  WiFi.begin(ssid, password);

  Serial.println("Conectando...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado.");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Cliente conectado.");
    while (client.connected()) {
      uint16_t value = analogRead(adcPin);
      client.write((uint8_t*)&value, sizeof(value));  // Envío binario: 2 bytes
      delayMicroseconds(1000);  // ~1000 muestras/s
    }
    client.stop();
    Serial.println("Cliente desconectado.");
  }
}
