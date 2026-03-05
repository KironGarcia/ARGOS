#!/usr/bin/env python3
"""
ARGOS Car - Menú de prueba de movimientos
Adelante / Atrás / Derecha / Esquerda (tracción diferencial)
Misma lógica que wheel_tests.py (direcciones + PWM).
Pinout: ENA Pin 37 (GPIO 26), ENB Pin 38 (GPIO 20)
"""

import RPi.GPIO as GPIO
import time

# ============================================================
# PINOUT (igual que wheel_tests.py)
# ============================================================
IN1 = 17   # Pin 11 - Motor A
IN2 = 27   # Pin 13 - Motor A
IN3 = 22   # Pin 15 - Motor B
IN4 = 23   # Pin 16 - Motor B
ENA = 26   # Pin 37 - PWM Motor A
ENB = 20   # Pin 38 - PWM Motor B

# Velocidades (como wheel_tests: 100% en giros, alto en recta)
SPEED_FWD = 80   # % adelante/atrás
SPEED_TURN = 100 # % giros (tracción diferencial)
DURATION = 2.0       # segundos adelante/atrás
DURATION_TURN = 0.5  # segundos giro (toque nomas, sin dar vueltas)

pwm_a = None
pwm_b = None


def setup_gpio():
    """Configuración inicial de GPIO y PWM"""
    global pwm_a, pwm_b
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

    GPIO.setup([ENA, ENB], GPIO.OUT)
    pwm_a = GPIO.PWM(ENA, 1000)
    pwm_b = GPIO.PWM(ENB, 1000)
    pwm_a.start(0)
    pwm_b.start(0)
    print("✅ GPIO configurado (ENA=Pin37, ENB=Pin38)")


def motor_stop():
    """Parar todos los motores (igual que wheel_tests)"""
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    if pwm_a and pwm_b:
        pwm_a.ChangeDutyCycle(0)
        pwm_b.ChangeDutyCycle(0)


# --- Direcciones y PWM igual que wheel_tests.py ---

def adelante():
    """Adelante: IN1=H IN2=L, IN3=H IN4=L + PWM 80%"""
    print("➡️  ADELANTE (2 s)...")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(SPEED_FWD)
    pwm_b.ChangeDutyCycle(SPEED_FWD)
    time.sleep(DURATION)
    motor_stop()


def atras():
    """Atrás: IN1=L IN2=H, IN3=L IN4=H + PWM 80%"""
    print("⬅️  ATRÁS (2 s)...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(SPEED_FWD)
    pwm_b.ChangeDutyCycle(SPEED_FWD)
    time.sleep(DURATION)
    motor_stop()


def derecha():
    """Derecha (tracción diferencial): Motor A atrás, Motor B adelante. Giro 0,5 s."""
    print("↪️  DERECHA (0,5 s)...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(SPEED_TURN)
    pwm_b.ChangeDutyCycle(SPEED_TURN)
    time.sleep(DURATION_TURN)
    motor_stop()


def esquerda():
    """Esquerda (tracción diferencial): Motor A adelante, Motor B atrás. Giro 0,5 s."""
    print("↩️  ESQUERDA (0,5 s)...")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(SPEED_TURN)
    pwm_b.ChangeDutyCycle(SPEED_TURN)
    time.sleep(DURATION_TURN)
    motor_stop()


def show_menu():
    """Muestra el menú y devuelve la opción elegida"""
    print()
    print("=" * 50)
    print("  ARGOS - Menú de movimientos")
    print("=" * 50)
    print("  1 - Adelante  (80%, 2 s)")
    print("  2 - Atrás     (80%, 2 s)")
    print("  3 - Derecha   (100%, 0,5 s)")
    print("  4 - Esquerda  (100%, 0,5 s)")
    print("  5 - Salir")
    print("=" * 50)
    return input("Elige (1-5): ").strip()


def cleanup():
    """Limpieza al salir"""
    motor_stop()
    if pwm_a:
        pwm_a.stop()
    if pwm_b:
        pwm_b.stop()
    GPIO.cleanup()
    print("🔧 GPIO limpio. Hasta luego.")


def main():
    print("🤖 ARGOS Car - Demo por menú")
    print("   Pinout: ENA=GPIO26 (Pin37), ENB=GPIO20 (Pin38)")
    setup_gpio()
    try:
        while True:
            opcion = show_menu()
            if opcion == "1":
                adelante()
            elif opcion == "2":
                atras()
            elif opcion == "3":
                derecha()
            elif opcion == "4":
                esquerda()
            elif opcion == "5":
                print("👋 Saliendo...")
                break
            else:
                print("❌ Opción no válida. Usa 1, 2, 3, 4 o 5.")
    except KeyboardInterrupt:
        print("\n👋 Interrompido (Ctrl+C)")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
