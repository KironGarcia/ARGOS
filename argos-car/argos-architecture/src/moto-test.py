#!/usr/bin/env python3
"""
PRUEBA MAESTRA - L298N Motor Test
Configuración: Jumpers ENA/ENB + Alimentación Dual 5V
"""

import RPi.GPIO as GPIO
import time

# Pines de dirección únicamente (ENA/ENB con jumpers)
IN1 = 17  # Physical Pin 11 - Motor A
IN2 = 27  # Physical Pin 13 - Motor A  
IN3 = 22  # Physical Pin 15 - Motor B
IN4 = 23  # Physical Pin 16 - Motor B

def setup():
    """Configuración inicial GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Configurar solo pines de dirección
    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
    
    # Estado inicial: motores parados
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("✅ GPIO configurado - Sistema listo")

def forward():
    """Ambos motores ADELANTE"""
    print("🚗 ADELANTE - Motor A + Motor B")
    GPIO.output(IN1, GPIO.HIGH)  # Motor A adelante
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)   # Motor B adelante (INVERTIDO)
    GPIO.output(IN4, GPIO.HIGH)

def backward():
    """Ambos motores ATRÁS"""
    print("🔄 ATRÁS - Motor A + Motor B")
    GPIO.output(IN1, GPIO.LOW)   # Motor A atrás
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)  # Motor B atrás (INVERTIDO)
    GPIO.output(IN4, GPIO.LOW)

def stop():
    """Parar todos los motores"""
    print("⏹️ STOP - Todos los motores")
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

def cleanup():
    """Limpieza final"""
    GPIO.cleanup()
    print("🔧 GPIO limpiado")

def main():
    print("🎯 PRUEBA MAESTRA L298N")
    print("=" * 50)
    print("CONFIGURACIÓN ACTUAL:")
    print(f"• IN1: GPIO {IN1} (Pin 11) - Motor A")
    print(f"• IN2: GPIO {IN2} (Pin 13) - Motor A")
    print(f"• IN3: GPIO {IN3} (Pin 15) - Motor B") 
    print(f"• IN4: GPIO {IN4} (Pin 16) - Motor B")
    print("• ENA/ENB: JUMPERS (velocidad máxima)")
    print("• Alimentación: DUAL 5V (jumper 5V_EN removido)")
    print("=" * 50)
    print("\n🚨 ATENCIÓN:")
    print("• Motores girarán a VELOCIDAD MÁXIMA")
    print("• Presiona Ctrl+C para parar en cualquier momento")
    print("• Observa la dirección de giro de cada motor")
    
    setup()
    
    try:
        input("\n🎬 Presiona ENTER para iniciar PRUEBA MAESTRA...")
        
        print("\n🔍 FASE 1: Test ADELANTE (5 segundos)")
        forward()
        time.sleep(5)
        
        print("\n🔍 FASE 2: PARAR (2 segundos)")
        stop()
        time.sleep(2)
        
        print("\n🔍 FASE 3: Test ATRÁS (5 segundos)")
        backward()
        time.sleep(5)
        
        print("\n🔍 FASE 4: PARAR final")
        stop()
        
        print("\n🎉 ¡PRUEBA MAESTRA COMPLETADA!")
        print("¿Los motores giraron correctamente?")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrumpido por usuario")
    finally:
        stop()
        cleanup()
        print("👋 Prueba maestra terminada")

if __name__ == "__main__":
    main() 