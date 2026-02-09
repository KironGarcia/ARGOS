#!/usr/bin/env python3
"""
Test de Dirección de Motores - ARGOS Car
Prueba cada motor individualmente a 30% de velocidad
Verifica si ambos van hacia adelante con la configuración actual
"""

import RPi.GPIO as GPIO
import time

# ============================================================
# CONFIGURACIÓN DE PINOS (PHYSICAL PIN NUMBERS)
# ============================================================

# Motor Controller L298N
# Physical Pin → GPIO
ENA = 26  # Pin 37 → GPIO 26 (Motor A Enable - PWM)
ENB = 20  # Pin 38 → GPIO 20 (Motor B Enable - PWM)
IN1 = 17  # Pin 11 → GPIO 17 (Motor A Direction 1)
IN2 = 27  # Pin 13 → GPIO 27 (Motor A Direction 2)
IN3 = 22  # Pin 15 → GPIO 22 (Motor B Direction 1)
IN4 = 23  # Pin 16 → GPIO 23 (Motor B Direction 2)

# ============================================================
# CONFIGURACIÓN DEL SISTEMA
# ============================================================

def setup_gpio():
    """Configuración inicial de GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Configurar pinos de dirección
    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    
    # Configurar pinos PWM
    GPIO.setup([ENA, ENB], GPIO.OUT)
    
    # Crear objetos PWM a 1000 Hz
    pwm_a = GPIO.PWM(ENA, 1000)
    pwm_b = GPIO.PWM(ENB, 1000)
    
    # Iniciar PWM en 0%
    pwm_a.start(0)
    pwm_b.start(0)
    
    print("✅ GPIO configurado correctamente")
    print(f"   ENA: GPIO {ENA} (Pin 37)")
    print(f"   ENB: GPIO {ENB} (Pin 38)")
    print(f"   IN1: GPIO {IN1} (Pin 11)")
    print(f"   IN2: GPIO {IN2} (Pin 13)")
    print(f"   IN3: GPIO {IN3} (Pin 15)")
    print(f"   IN4: GPIO {IN4} (Pin 16)")
    
    return pwm_a, pwm_b

def cleanup_gpio(pwm_a, pwm_b):
    """Limpiar GPIO al finalizar"""
    pwm_a.stop()
    pwm_b.stop()
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    GPIO.cleanup()
    print("🔧 GPIO limpio")

# ============================================================
# FUNCIONES DE TEST
# ============================================================

def test_motor_a(pwm_a, speed=30):
    """
    Test Motor A (OUT1, OUT2)
    Debe girar hacia ADELANTE
    """
    print("\n" + "=" * 60)
    print("🔧 TEST MOTOR A - Salidas OUT1 y OUT2 del L298N")
    print("=" * 60)
    print(f"⚡ Velocidad: {speed}%")
    print("📍 Dirección: ADELANTE")
    print("   IN1 = HIGH, IN2 = LOW")
    print("=" * 60)
    
    input("➡️  Presiona ENTER para iniciar Motor A...")
    
    # Configurar dirección: ADELANTE
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    
    # Activar PWM al porcentaje especificado
    pwm_a.ChangeDutyCycle(speed)
    
    print(f"\n🚗 Motor A girando a {speed}% por 3 segundos...")
    time.sleep(3)
    
    # Parar motor
    pwm_a.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    
    print("⏹️  Motor A detenido")
    
    # Pregunta de verificación
    print("\n" + "=" * 60)
    response = input("❓ ¿El Motor A giró hacia ADELANTE? (s/n): ").lower().strip()
    
    if response == 's' or response == 'sim':
        print("✅ Motor A: Dirección CORRECTA")
        return True
    else:
        print("❌ Motor A: Dirección INCORRECTA - Cables invertidos")
        return False

def test_motor_b(pwm_b, speed=30):
    """
    Test Motor B (OUT3, OUT4)
    Debe girar hacia ADELANTE
    """
    print("\n" + "=" * 60)
    print("🔧 TEST MOTOR B - Salidas OUT3 y OUT4 del L298N")
    print("=" * 60)
    print(f"⚡ Velocidad: {speed}%")
    print("📍 Dirección: ADELANTE")
    print("   IN3 = HIGH, IN4 = LOW")
    print("=" * 60)
    
    input("➡️  Presiona ENTER para iniciar Motor B...")
    
    # Configurar dirección: ADELANTE
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    
    # Activar PWM al porcentaje especificado
    pwm_b.ChangeDutyCycle(speed)
    
    print(f"\n🚗 Motor B girando a {speed}% por 3 segundos...")
    time.sleep(3)
    
    # Parar motor
    pwm_b.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    
    print("⏹️  Motor B detenido")
    
    # Pregunta de verificación
    print("\n" + "=" * 60)
    response = input("❓ ¿El Motor B giró hacia ADELANTE? (s/n): ").lower().strip()
    
    if response == 's' or response == 'sim':
        print("✅ Motor B: Dirección CORRECTA")
        return True
    else:
        print("❌ Motor B: Dirección INCORRECTA - Cables invertidos")
        return False

def test_both_motors(pwm_a, pwm_b, speed=30):
    """
    Test ambos motores simultáneamente
    Ambos deben girar hacia ADELANTE
    """
    print("\n" + "=" * 60)
    print("🔧 TEST AMBOS MOTORES - Simultáneamente")
    print("=" * 60)
    print(f"⚡ Velocidad: {speed}%")
    print("📍 Dirección: ADELANTE (ambos)")
    print("=" * 60)
    
    input("➡️  Presiona ENTER para iniciar ambos motores...")
    
    # Configurar dirección: ADELANTE
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    
    # Activar PWM al porcentaje especificado
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    
    print(f"\n🚗 Ambos motores girando a {speed}% por 3 segundos...")
    time.sleep(3)
    
    # Parar motores
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    
    print("⏹️  Ambos motores detenidos")

# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("🤖 ARGOS CAR - TEST DE DIRECCIÓN DE MOTORES")
    print("=" * 60)
    print("Objetivo: Verificar direcciones de motores")
    print("Velocidad de test: 30%")
    print("=" * 60)
    print("\n⚠️  IMPORTANTE:")
    print("   • Coloca el carro en posición elevada")
    print("   • Asegúrate de que las ruedas puedan girar libremente")
    print("   • Observa la dirección de giro de cada rueda")
    print("=" * 60)
    
    input("\n✅ Presiona ENTER cuando estés listo para continuar...")
    
    # Configurar GPIO y PWM
    pwm_a, pwm_b = setup_gpio()
    
    try:
        # Test Motor A
        motor_a_ok = test_motor_a(pwm_a, speed=30)
        time.sleep(2)
        
        # Test Motor B
        motor_b_ok = test_motor_b(pwm_b, speed=30)
        time.sleep(2)
        
        # Test ambos juntos
        test_both_motors(pwm_a, pwm_b, speed=30)
        
        # Resumen de resultados
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        if motor_a_ok:
            print("✅ Motor A: Dirección correcta (OUT1/OUT2)")
        else:
            print("❌ Motor A: Invertir cables en OUT1 y OUT2")
        
        if motor_b_ok:
            print("✅ Motor B: Dirección correcta (OUT3/OUT4)")
        else:
            print("❌ Motor B: Invertir cables en OUT3 y OUT4")
        
        print("=" * 60)
        
        if motor_a_ok and motor_b_ok:
            print("\n🎉 ¡AMBOS MOTORES CONFIGURADOS CORRECTAMENTE!")
            print("✅ Puedes proceder con los tests de tração diferencial")
        else:
            print("\n⚠️  ACCIÓN REQUERIDA:")
            print("   1. Invierte los cables físicamente en las salidas")
            print("      del L298N que están incorrectas")
            print("   2. Vuelve a ejecutar este test para confirmar")
        
        print("=" * 60)
        
        # Nota sobre PWM
        print("\n📝 NOTA SOBRE PWM:")
        print(f"   • ENA (Pin 37/GPIO 26): {'Funciona bien' if motor_a_ok else 'Verificar señal'} ✅")
        print(f"   • ENB (Pin 38/GPIO 20): {'Funciona bien' if motor_b_ok else 'Verificar señal'} ✅")
        print("   • Ambos pines son general purpose (sin conflictos)")
        print("   • Configuración óptima para PWM de motores")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por usuario")
    
    finally:
        cleanup_gpio(pwm_a, pwm_b)
        print("\n👋 Test finalizado")

if __name__ == "__main__":
    main()

