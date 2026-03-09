/*
 * OTA WiFi — Alexa China (ESP32)
 * Conecta à rede WiFi e activa actualização Over-The-Air (OTA).
 * Gravar este sketch UMA VEZ por USB; depois podes enviar código pela rede.
 *
 * GUIA PASSO A PASSO (resumo no final do ficheiro).
 */

#include <WiFi.h>
#include <ArduinoOTA.h>

// ——— Configuração: edita com a tua rede ———
#define WIFI_SSID     "O_TEU_SSID"
#define WIFI_PASSWORD "A_TUA_PASSWORD"

#define OTA_HOSTNAME  "alexa-china"   // Nome do ESP32 na rede (opcional)

#define WIFI_TIMEOUT_MS  20000   // 20 s; se não ligar, desiste e imprime erro

void setup() {
  // 1) Serial o mais cedo possível e mensagem imediata (para confirmação no Monitor)
  Serial.begin(115200);
  delay(800);   // dar tempo ao USB-Serial estabilizar
  Serial.println();
  Serial.println(F("========================================"));
  Serial.println(F("  BOOT - OTA WiFi (Alexa China)"));
  Serial.println(F("  Baud: 115200"));
  Serial.println(F("========================================"));
  Serial.flush();
  delay(1500);   // tempo para abrires o Monitor Serial

  // 2) Tentar WiFi
  Serial.println(F("\n[1/2] WiFi"));
  Serial.print(F("      SSID: "));
  Serial.println(WIFI_SSID);
  Serial.print(F("      A ligar"));
  Serial.flush();

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - t0 > WIFI_TIMEOUT_MS) {
      Serial.println();
      Serial.println(F("      ERRO: Timeout. Verifica SSID e password."));
      Serial.println(F("      A reiniciar em 5 s..."));
      Serial.flush();
      delay(5000);
      ESP.restart();
    }
    delay(400);
    Serial.print('.');
    Serial.flush();
  }
  Serial.println(F(" OK"));
  Serial.print(F("      IP: "));
  Serial.println(WiFi.localIP());
  Serial.flush();

  // 3) OTA
  Serial.println(F("\n[2/2] OTA"));
  ArduinoOTA.setHostname(OTA_HOSTNAME);
  ArduinoOTA
    .onStart([]() {
      Serial.println(F("      OTA: actualização a começar..."));
    })
    .onEnd([]() {
      Serial.println(F("      OTA: actualização concluída."));
    })
    .onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("      OTA: %u%%\r", (progress / (total / 100)));
    })
    .onError([](ota_error_t error) {
      Serial.printf("      OTA erro [%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println(F("Auth"));
      else if (error == OTA_BEGIN_ERROR) Serial.println(F("Begin"));
      else if (error == OTA_CONNECT_ERROR) Serial.println(F("Connect"));
      else if (error == OTA_RECEIVE_ERROR) Serial.println(F("Receive"));
      else if (error == OTA_END_ERROR) Serial.println(F("End"));
    });

  ArduinoOTA.begin();
  Serial.println(F("      OTA activo."));
  Serial.println();
  Serial.println(F(">>> ANOTA O IP ACIMA PARA A ARDUINO IDE <<<"));
  Serial.println(F(">>> OTA pronto. Podes carregar por rede.    <<<"));
  Serial.println();
  Serial.flush();
}

void loop() {
  ArduinoOTA.handle();
}

/*
 * ========== GUIA PASSO A PASSO — OTA no ESP32 ==========
 *
 * PASSO 1 — Primeira gravação (por USB)
 *   • Abre este sketch na Arduino IDE.
 *   • Em cima, altera WIFI_SSID e WIFI_PASSWORD para a tua rede (a mesma da Pi).
 *   • Ferramentas → Placa → ESP32 Arduino → "ESP32 Dev Module" (ou a tua placa).
 *   • Ferramentas → Porta → escolhe a porta USB do ESP32 (ex.: /dev/ttyUSB0).
 *   • Liga o ESP32 ao portátil por cabo USB (dados).
 *   • Clica em "Carregar".
 *   • Abre o Monitor Serial (115200 baud). Anota o IP que aparecer (ex.: 192.168.0.10).
 *
 * PASSO 2 — Usar OTA daqui em diante
 *   • Desliga o cabo USB. Alimenta o ESP32 pelo powerbank (cabo cortado), para ter GND comum com LEDs/SD.
 *   • O ESP32 liga à WiFi e fica à espera de OTA.
 *   • Na Arduino IDE: Ferramentas → Porta.
 *     - Se aparecer "Portas de rede" / "Network Ports", escolhe "Introduzir endereço IP" (ou similar) e escreve o IP do ESP32 (ex.: 192.168.0.10).
 *     - Ou escolhe directamente "esp32 at 192.168.0.10" se a IDE o mostrar.
 *   • Clica em "Carregar" outra vez. O código será enviado pela WiFi; não precisas de USB.
 *
 * PASSO 3 — Manter OTA noutros sketches
 *   • Quando fores usar outro sketch (ex.: 1test, teste_só_luces), copia para esse sketch:
 *     - #include <WiFi.h> e #include <ArduinoOTA.h>
 *     - As mesmas variáveis WIFI_SSID, WIFI_PASSWORD e OTA_HOSTNAME.
 *     - No setup(): o bloco WiFi.begin(...) até WiFi.localIP() e o bloco ArduinoOTA.setHostname(...) até ArduinoOTA.begin().
 *     - No loop(): ArduinoOTA.handle(); (pode ser a primeira linha do loop).
 *   • Assim continuas a poder fazer upload por rede nesse sketch também.
 *
 * NOTA: ESP32 e portátil (ou Pi) têm de estar na mesma rede WiFi.
 */
