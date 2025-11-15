#!/usr/bin/env python3
"""
HC-SR04 Sensor Test
Verificación de funcionamiento del sensor ultrasónico
"""

import RPi.GPIO as GPIO
import time

# Pin definitions
TRIG_PIN = 24  # Physical Pin 18
ECHO_PIN = 10  # Physical Pin 19

def setup():
    """Configuración inicial GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    
    # Estado inicial: TRIG en LOW
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.1)  # Estabilizar sensor
    print("✅ Sensor HC-SR04 configurado - Sistema listo")

def measure_distance():
    """Medir distancia en centímetros"""
    # Enviar pulso de disparo (10µs mínimo)
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microsegundos
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Esperar inicio del pulso ECHO
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    
    # Esperar fin del pulso ECHO
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    
    # Calcular duración del pulso
    pulse_duration = pulse_end - pulse_start
    
    # Convertir a distancia (cm)
    # Velocidad del sonido: 34300 cm/s
    distance = (pulse_duration * 34300) / 2
    
    return round(distance, 2)

def cleanup():
    """Limpieza final"""
    GPIO.cleanup()
    print("🔧 GPIO limpiado")

def main():
    print("🎯 TEST SENSOR HC-SR04")
    print("=" * 40)
    print("CONFIGURACIÓN:")
    print(f"• TRIG: GPIO {TRIG_PIN} (Pin 18)")
    print(f"• ECHO: GPIO {ECHO_PIN} (Pin 19)")
    print("• Umbral: 30cm")
    print("• Presiona Ctrl+C para parar")
    print("=" * 40)
    
    setup()
    
    # Variables para control de mensajes
    obstacle_detected = False
    
    try:
        print("\n📡 Iniciando detección de obstáculos...")
        print("Mueve objetos cerca del sensor para probar\n")
        
        while True:
            distance = measure_distance()
            
            # Verificar si hay obstáculo
            if distance < 30:
                if not obstacle_detected:
                    print("🚨 OBSTÁCULO DETECTADO - Distancia:", distance, "cm")
                    obstacle_detected = True
            else:
                if obstacle_detected:
                    print("✅ CAMINO LIBRE - Distancia:", distance, "cm")
                    obstacle_detected = False
                else:
                    print("📏 Distancia:", distance, "cm")
            
            time.sleep(0.5)  # Pausa entre mediciones
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrumpido por usuario")
    finally:
        cleanup()
        print("👋 Test del sensor terminado")

if __name__ == "__main__":
    main()
