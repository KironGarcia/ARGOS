/*
 * Sketch de teste completo — Alexa China (ESP32)
 * Menu Serial: microfone, amplificador/parlante, luzes.
 * Pines: LED amarelo=5, LED vermelho=18 | I2S: WS=15, SCK=14, SD=13 | DAC=25
 */

#include "driver/i2s.h"

// ——— Pines do proyecto ———
#define LED_AMARELO  5
#define LED_VERMELHO 18
#define I2S_WS       15
#define I2S_SCK      14
#define I2S_SD       13
#define DAC_PIN      25

// I2S para INMP441 (micrófono)
#define I2S_PORT     I2S_NUM_0
#define SAMPLE_RATE  16000
#define SAMPLE_BITS  16
#define DMA_BUF_LEN  1024
#define DMA_BUF_CNT  2

static bool i2s_iniciado = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  pinMode(DAC_PIN, OUTPUT);
  delay(500);
  imprimirMenu();
}

void loop() {
  if (Serial.available()) {
    char op = Serial.read();
    while (Serial.read() != -1) { } // limpar buffer

    if (op == '1') {
      testarMicrofone(1);
    } else if (op == '2') {
      testarParlante(2);
    } else if (op == '3') {
      testarLuces(3);
    } else {
      Serial.println(F("Opção inválida. Digite 1, 2 ou 3."));
    }
    imprimirMenu();
  }
  delay(50);
}

// ——— Menú ———
void imprimirMenu() {
  Serial.println();
  Serial.println(F("========== MENU DE TESTES =========="));
  Serial.println(F("1 - Testar microfone (INMP441 I2S)"));
  Serial.println(F("2 - Testar amplificador/parlante (DAC)"));
  Serial.println(F("3 - Testar luces (LEDs)"));
  Serial.println(F("====================================="));
  Serial.print(F("Escolha (1/2/3): "));
}

// ——— Teste de luces (5 s, fade em conjunto) ———
void fadeLED(int pin, int startVal, int endVal, int durationMs) {
  int steps = abs(endVal - startVal);
  if (steps == 0) return;
  int delayTime = durationMs / steps;
  if (delayTime < 1) delayTime = 1;

  if (startVal < endVal) {
    for (int i = startVal; i <= endVal; i++) {
      analogWrite(LED_AMARELO, i);
      analogWrite(LED_VERMELHO, i);
      delay(delayTime);
    }
  } else {
    for (int i = startVal; i >= endVal; i--) {
      analogWrite(LED_AMARELO, i);
      analogWrite(LED_VERMELHO, i);
      delay(delayTime);
    }
  }
}

void testarLuces(int) {
  Serial.println(F("\n--- Teste de luces (5 s) ---"));
  const int meio = 2500; // 2,5 s subida + 2,5 s descida = 5 s
  fadeLED(LED_AMARELO, 0, 255, meio);
  fadeLED(LED_AMARELO, 255, 0, meio);
  analogWrite(LED_AMARELO, 0);
  analogWrite(LED_VERMELHO, 0);

  perguntarDeNovoOuMenu(3);
}

// ——— Teste de microfone (I2S INMP441, 5 s, mostrar níveis) ———
bool iniciarI2SMicrofone() {
  if (i2s_iniciado) return true;

  i2s_config_t cfg = {};
  cfg.mode                 = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX);
  cfg.sample_rate          = SAMPLE_RATE;
  cfg.bits_per_sample      = I2S_BITS_PER_SAMPLE_16BIT;
  cfg.channel_format       = I2S_CHANNEL_FMT_ONLY_LEFT;
  cfg.communication_format = I2S_COMM_FORMAT_STAND_I2S;
  cfg.intr_alloc_flags     = 0;
  cfg.dma_buf_count        = DMA_BUF_CNT;
  cfg.dma_buf_len          = DMA_BUF_LEN;
  cfg.use_apll             = false;

  i2s_pin_config_t pin = {};
  pin.bck_io_num   = I2S_SCK;
  pin.ws_io_num    = I2S_WS;
  pin.data_out_num = I2S_PIN_NO_CHANGE;
  pin.data_in_num  = I2S_SD;

  esp_err_t err = i2s_driver_install(I2S_PORT, &cfg, 0, NULL);
  if (err != ESP_OK) {
    Serial.printf("Erro I2S install: %d\n", err);
    return false;
  }
  err = i2s_set_pin(I2S_PORT, &pin);
  if (err != ESP_OK) {
    Serial.printf("Erro I2S set_pin: %d\n", err);
    i2s_driver_uninstall(I2S_PORT);
    return false;
  }
  i2s_zero_dma_buffer(I2S_PORT);
  i2s_iniciado = true;
  return true;
}

void pararI2S() {
  if (!i2s_iniciado) return;
  i2s_driver_uninstall(I2S_PORT);
  i2s_iniciado = false;
}

void testarMicrofone(int opcaoMenu) {
  Serial.println(F("\n--- Teste de microfone (5 s) ---"));
  if (!iniciarI2SMicrofone()) {
    Serial.println(F("Falha ao iniciar I2S. Verifique conexões (WS=15, SCK=14, SD=13)."));
    perguntarDeNovoOuMenu(opcaoMenu);
    return;
  }

  const unsigned long duracaoMs = 5000;
  const unsigned long inicio = millis();
  int32_t soma = 0;
  uint32_t numAmostras = 0;
  int32_t pico = 0;
  int16_t buf[DMA_BUF_LEN];
  size_t lidos;

  Serial.println(F("Gravando 5 segundos... fale ou faça barulho."));

  while (millis() - inicio < duracaoMs) {
    esp_err_t err = i2s_read(I2S_PORT, buf, sizeof(buf), &lidos, portMAX_DELAY);
    if (err != ESP_OK || lidos == 0) continue;

    uint32_t n = lidos / sizeof(int16_t);
    for (uint32_t i = 0; i < n; i++) {
      int32_t v = (int32_t)buf[i];
      if (v < 0) v = -v;
      soma += v;
      if (v > pico) pico = v;
      numAmostras++;
    }

    // A cada ~200 ms mostrar um valor para feedback em tempo real
    static unsigned long ultimoPrint = 0;
    if (millis() - ultimoPrint >= 200) {
      Serial.printf("  [%lu ms] amostras: %lu, pico até agora: %ld\n",
                    (unsigned long)(millis() - inicio), numAmostras, (long)pico);
      ultimoPrint = millis();
    }
  }

  int32_t nivelMedio = numAmostras > 0 ? (soma / (int32_t)numAmostras) : 0;
  Serial.println(F("--- Resultado do microfone ---"));
  Serial.printf("  Nível médio: %ld\n", (long)nivelMedio);
  Serial.printf("  Pico: %ld\n", (long)pico);
  Serial.printf("  Total de amostras: %lu\n", (unsigned long)numAmostras);
  Serial.println(F("Se os números mudaram ao falar, o microfone está a funcionar."));

  perguntarDeNovoOuMenu(1);
}

// ——— Teste de parlante (DAC 25, tono que sobe de frequência) ———
void testarParlante(int opcaoMenu) {
  Serial.println(F("\n--- Teste de parlante (DAC, ~5 s) ---"));
  Serial.println(F("Deve ouvir um tom que sobe de frequência."));

  const unsigned long duracaoMs = 5000;
  const unsigned long inicio = millis();
  const int freqMin = 200;
  const int freqMax = 2000;

  while (millis() - inicio < duracaoMs) {
    unsigned long t = millis() - inicio;
    // Frequência sobe linearmente de freqMin a freqMax
    int freq = freqMin + (int)((long)(freqMax - freqMin) * (long)t / (long)duracaoMs);
    if (freq > freqMax) freq = freqMax;

    int meioPeriodoUs = 500000 / freq;
    if (meioPeriodoUs < 10) meioPeriodoUs = 10;

    // Onda quadrada no DAC durante um curto intervalo (para manter sweep suave)
    unsigned long blocoAte = millis() + 50;
    while (millis() < blocoAte && (millis() - inicio) < duracaoMs) {
      dacWrite(DAC_PIN, 0);
      delayMicroseconds(meioPeriodoUs);
      dacWrite(DAC_PIN, 255);
      delayMicroseconds(meioPeriodoUs);
    }
  }

  dacWrite(DAC_PIN, 0);
  Serial.println(F("Fim do som."));

  perguntarDeNovoOuMenu(2);
}

// ——— Perguntar: repetir teste ou voltar ao menú ———
void perguntarDeNovoOuMenu(int opcaoTesteAtual) {
  Serial.println();
  Serial.print(F("Testar de novo (1) ou voltar ao menu (2)? "));

  unsigned long t0 = millis();
  while (millis() - t0 < 30000) {
    if (Serial.available()) {
      char c = Serial.read();
      while (Serial.read() != -1) { }
      if (c == '1') {
        if (opcaoTesteAtual == 1) testarMicrofone(1);
        else if (opcaoTesteAtual == 2) testarParlante(2);
        else if (opcaoTesteAtual == 3) testarLuces(3);
        return;
      }
      if (c == '2') {
        break;
      }
      Serial.print(F("Digite 1 ou 2: "));
      t0 = millis();
    }
    delay(50);
  }
  Serial.println();
  imprimirMenu();
}
