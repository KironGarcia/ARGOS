/*
 * Teste APENAS das luces (LEDs) — Alexa China (ESP32)
 * Sem microfone, sem parlante. Só LEDs em fade junto (5 s).
 * Pines: LED amarelo = 5, LED vermelho = 18
 */

#define LED_AMARELO  5
#define LED_VERMELHO 18

void setup() {
  Serial.begin(115200);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  analogWrite(LED_AMARELO, 0);
  analogWrite(LED_VERMELHO, 0);
  delay(500);
  Serial.println(F("=== Teste SÓ LUCES ===\nAs duas luces vão subir e descer em fade (5 s).\n"));
}

void loop() {
  // 2,5 s subida + 2,5 s descida = 5 s total; as duas juntas
  const int meio = 2500;

  for (int i = 0; i <= 255; i++) {
    analogWrite(LED_AMARELO, i);
    analogWrite(LED_VERMELHO, i);
    delay(meio / 255);
  }
  for (int i = 255; i >= 0; i--) {
    analogWrite(LED_AMARELO, i);
    analogWrite(LED_VERMELHO, i);
    delay(meio / 255);
  }

  analogWrite(LED_AMARELO, 0);
  analogWrite(LED_VERMELHO, 0);
  delay(500);
}
