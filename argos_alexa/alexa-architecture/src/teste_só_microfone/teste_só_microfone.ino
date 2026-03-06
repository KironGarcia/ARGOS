/*
 * Teste APENAS do microfone (INMP441 I2S) — Alexa China (ESP32)
 * Pergunta se inicia; grava 10 s; analisa e diz se funcionou ou não.
 * Pines: WS=15, SCK=14, SD=13
 */

#include "driver/i2s.h"

#define I2S_WS       15
#define I2S_SCK      14
#define I2S_SD       13
#define I2S_PORT     I2S_NUM_0
#define SAMPLE_RATE  16000
#define DMA_BUF_LEN  1024
#define DMA_BUF_CNT  2

// Limiares para decidir "funcionou": pico e nível médio mínimos quando há voz
#define PICO_MINIMO_VOZ      1500
#define NIVEL_MEDIO_MINIMO  200

static bool i2s_iniciado = false;

bool iniciarI2S() {
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

  if (i2s_driver_install(I2S_PORT, &cfg, 0, NULL) != ESP_OK) return false;
  if (i2s_set_pin(I2S_PORT, &pin) != ESP_OK) {
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

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println(F("========================================"));
  Serial.println(F("  Teste SÓ MICROFONE (INMP441 I2S)"));
  Serial.println(F("========================================"));
  Serial.println(F("Grava 10 segundos e analisa se captou voz."));
  Serial.println();
}

void loop() {
  Serial.println(F("Iniciar prova? (s = sim, n = não)"));
  Serial.print(F("> "));

  while (!Serial.available()) { delay(50); }
  char c = Serial.read();
  while (Serial.read() != -1) { }

  if (c != 's' && c != 'S') {
    Serial.println(F("Cancelado. Digite 's' para iniciar a prova."));
    return;
  }

  Serial.println(F("\n--- Iniciando prova de 10 segundos ---"));
  if (!iniciarI2S()) {
    Serial.println(F("ERRO: Falha ao iniciar I2S. Verifique conexões (WS=15, SCK=14, SD=13)."));
    Serial.println(F("Resultado: MICROFONE NÃO FUNCIONOU (falha de hardware/configuração)."));
    return;
  }

  Serial.println(F("Fale perto do microfone agora..."));

  const unsigned long duracaoMs = 10000;
  const unsigned long inicio = millis();
  int32_t soma = 0;
  uint32_t numAmostras = 0;
  int32_t pico = 0;
  int16_t buf[DMA_BUF_LEN];
  size_t lidos;

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
  }

  pararI2S();

  int32_t nivelMedio = numAmostras > 0 ? (soma / (int32_t)numAmostras) : 0;

  // Análise: consideramos "funcionou" se houve sinal forte (voz) em algum momento
  bool funcionou = (pico >= PICO_MINIMO_VOZ) && (nivelMedio >= NIVEL_MEDIO_MINIMO);

  Serial.println(F("\n--- Resultado da análise ---"));
  Serial.printf("  Nível médio: %ld\n", (long)nivelMedio);
  Serial.printf("  Pico: %ld\n", (long)pico);
  Serial.printf("  Amostras: %lu\n", (unsigned long)numAmostras);
  Serial.println();

  if (funcionou) {
    Serial.println(F(">>> MICROFONE FUNCIONOU <<<"));
    Serial.println(F("    O microfone captou sinal compatível com voz."));
  } else {
    Serial.println(F(">>> MICROFONE NÃO FUNCIONOU (ou sem voz detectada) <<<"));
    Serial.println(F("    Possíveis causas: não falou perto, conexões I2S, ou mic desligado."));
    Serial.println(F("    Se falou e deu isto, verifique WS=15, SCK=14, SD=13 e alimentação 3V3."));
  }

  Serial.println();
}
