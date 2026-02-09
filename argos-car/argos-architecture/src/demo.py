#!/usr/bin/env python3
"""
Demo de Testes - ARGOS Car
Sistema de testes para validação de tração diferencial e navegação autônoma
"""

import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO DOS PINOS
# ============================================================

# Pinos do Motor L298N
ENA = 26  # Physical Pin 37 - Motor A Enable (PWM)
ENB = 20  # Physical Pin 38 - Motor B Enable (PWM)
IN1 = 17  # Physical Pin 11 - Motor A Direction 1
IN2 = 27  # Physical Pin 13 - Motor A Direction 2
IN3 = 22  # Physical Pin 15 - Motor B Direction 1
IN4 = 23  # Physical Pin 16 - Motor B Direction 2

# Pinos do Sensor HC-SR04
TRIG_PIN = 10  # Physical Pin 19 - GPIO 10 (MOSI)
ECHO_PIN = 9   # Physical Pin 21 - GPIO 9 (MISO)

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================

sensor_running = False
sensor_thread = None
current_distance = 999  # Distância inicial alta (sem obstáculo)

# ============================================================
# CONFIGURAÇÃO DO SISTEMA
# ============================================================

def setup_gpio():
    """Configuração inicial dos GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Configurar pinos dos motores (direção)
    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    
    # Configurar pinos PWM (enable) com controle de velocidade
    GPIO.setup([ENA, ENB], GPIO.OUT)
    
    # Criar objetos PWM (1000 Hz)
    pwm_a = GPIO.PWM(ENA, 1000)
    pwm_b = GPIO.PWM(ENB, 1000)
    
    # Iniciar PWM em 0%
    pwm_a.start(0)
    pwm_b.start(0)
    
    # Configurar pinos do sensor
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    print("✅ GPIO configurado com controle PWM")
    
    return pwm_a, pwm_b

def cleanup_gpio(pwm_a, pwm_b):
    """Limpeza dos GPIO"""
    motor_stop(pwm_a, pwm_b)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("🔧 GPIO limpo")

# ============================================================
# CONTROLE DOS MOTORES
# ============================================================

def motor_forward(pwm_a, pwm_b, speed=30):
    """
    Motores para frente com controle de velocidade
    Arranque forte (50%) por 0.3s, depois velocidade controlada
    """
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    
    # Arranque forte a 50%
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    time.sleep(0.3)  # 300ms de arranque forte
    
    # Reduzir para velocidade controlada
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def motor_backward(pwm_a, pwm_b, speed=30):
    """
    Motores para trás com controle de velocidade
    Arranque forte (50%) por 0.3s, depois velocidade controlada
    """
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    
    # Arranque forte a 50%
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    time.sleep(0.3)  # 300ms de arranque forte
    
    # Reduzir para velocidade controlada
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def motor_stop(pwm_a, pwm_b):
    """Parar todos os motores"""
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

def differential_right(pwm_a, pwm_b, speed=50):
    """Tração diferencial para DIREITA"""
    # Motor esquerdo para frente, motor direito para trás
    GPIO.output(IN1, GPIO.HIGH)  # Motor A (esquerdo) frente
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)   # Motor B (direito) trás
    GPIO.output(IN4, GPIO.HIGH)
    
    # Aplicar velocidade para giro
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def differential_left(pwm_a, pwm_b, speed=50):
    """Tração diferencial para ESQUERDA"""
    # Motor direito para frente, motor esquerdo para trás
    GPIO.output(IN1, GPIO.LOW)   # Motor A (esquerdo) trás
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)  # Motor B (direito) frente
    GPIO.output(IN4, GPIO.LOW)
    
    # Aplicar velocidade para giro
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

# ============================================================
# SENSOR ULTRASSÔNICO
# ============================================================

def measure_distance():
    """Medir distância com sensor HC-SR04"""
    try:
        # Enviar pulso de disparo
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microsegundos
        GPIO.output(TRIG_PIN, GPIO.LOW)
        
        # Medir tempo do pulso ECHO
        pulse_start = time.time()
        timeout_start = time.time()
        while GPIO.input(ECHO_PIN) == GPIO.LOW:
            pulse_start = time.time()
            if time.time() - timeout_start > 0.1:  # Timeout 100ms
                return 999
        
        pulse_end = time.time()
        timeout_start = time.time()
        while GPIO.input(ECHO_PIN) == GPIO.HIGH:
            pulse_end = time.time()
            if time.time() - timeout_start > 0.1:  # Timeout 100ms
                return 999
        
        # Calcular distância
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2
        
        return round(distance, 2)
    except:
        return 999

def sensor_monitor():
    """Thread para monitoramento contínuo do sensor"""
    global current_distance, sensor_running
    
    while sensor_running:
        try:
            current_distance = measure_distance()
            time.sleep(0.05)  # Verificar a cada 50ms
        except Exception as e:
            print(f"❌ Erro no sensor: {e}")
            time.sleep(0.1)

def start_sensor():
    """Iniciar monitoramento do sensor"""
    global sensor_running, sensor_thread
    
    if not sensor_running:
        sensor_running = True
        sensor_thread = threading.Thread(target=sensor_monitor, daemon=True)
        sensor_thread.start()
        time.sleep(0.2)
        print("📡 Sensor ativado")

def stop_sensor():
    """Parar monitoramento do sensor"""
    global sensor_running
    sensor_running = False
    if sensor_thread:
        time.sleep(0.2)
    print("📡 Sensor desativado")

# ============================================================
# TESTE 1: PRUEBA DE CURVA
# ============================================================

def test_curve(pwm_a, pwm_b, direction):
    """
    Teste de curva com tração diferencial
    
    Args:
        pwm_a: Objeto PWM do Motor A
        pwm_b: Objeto PWM do Motor B
        direction: 'direita' ou 'esquerda'
    """
    print("\n" + "=" * 60)
    print(f"🔄 INICIANDO TESTE DE CURVA - Direção: {direction.upper()}")
    print("=" * 60)
    print("⚡ Velocidade: Arranque 50% → Controlada 30%")
    
    try:
        # Fase 1: Motor por 3 segundos (arranque 50% → 30%)
        print("\n➡️  Fase 1: Avançando por 3 segundos...")
        print("   (Arranque 50% por 0.3s → 30% controlada)")
        motor_forward(pwm_a, pwm_b, speed=30)
        time.sleep(3)
        
        # Fase 2: Tração diferencial por 0.5 segundos
        print(f"\n🔄 Fase 2: Executando curva à {direction} (0.5s a 50%)...")
        if direction == 'direita':
            differential_right(pwm_a, pwm_b, speed=50)
        else:
            differential_left(pwm_a, pwm_b, speed=50)
        time.sleep(0.5)
        
        # Fase 3: Motor normal por 3 segundos
        print("\n➡️  Fase 3: Voltando à rotação normal por 3 segundos...")
        motor_forward(pwm_a, pwm_b, speed=30)
        time.sleep(3)
        
        # Fase 4: Parar motor
        print("\n⏹️  Fase 4: Parando motor...")
        motor_stop(pwm_a, pwm_b)
        
        print("\n✅ TESTE DE CURVA CONCLUÍDO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        motor_stop(pwm_a, pwm_b)

def menu_test_curve(pwm_a, pwm_b):
    """Menu de teste de curva com seleção de direção"""
    while True:
        print("\n" + "=" * 60)
        print("🔄 MENU: PRUEBA DE CURVA")
        print("=" * 60)
        print("1. Teste com giro à DIREITA")
        print("2. Teste com giro à ESQUERDA")
        print("3. Voltar ao menu principal")
        print("=" * 60)
        
        choice = input("\n❓ Escolha uma opção (1-3): ").strip()
        
        if choice == '1':
            test_curve(pwm_a, pwm_b, 'direita')
            
            # Perguntar se quer repetir
            while True:
                repeat = input("\n❓ Deseja fazer o teste novamente? (s/n): ").lower().strip()
                if repeat == 's' or repeat == 'sim':
                    test_curve(pwm_a, pwm_b, 'direita')
                elif repeat == 'n' or repeat == 'nao' or repeat == 'não':
                    break
                else:
                    print("❌ Resposta inválida. Digite 's' para sim ou 'n' para não.")
        
        elif choice == '2':
            test_curve(pwm_a, pwm_b, 'esquerda')
            
            # Perguntar se quer repetir
            while True:
                repeat = input("\n❓ Deseja fazer o teste novamente? (s/n): ").lower().strip()
                if repeat == 's' or repeat == 'sim':
                    test_curve(pwm_a, pwm_b, 'esquerda')
                elif repeat == 'n' or repeat == 'nao' or repeat == 'não':
                    break
                else:
                    print("❌ Resposta inválida. Digite 's' para sim ou 'n' para não.")
        
        elif choice == '3':
            print("↩️  Voltando ao menu principal...")
            break
        
        else:
            print("❌ Opção inválida. Escolha 1, 2 ou 3.")

# ============================================================
# TESTE 2: PRUEBA COMPLETA
# ============================================================

def test_complete(pwm_a, pwm_b):
    """
    Teste completo de navegação autônoma com desvio de obstáculos
    
    Duração: 6 segundos
    - Se obstáculo a 70cm: freia e espera
    - Se obstáculo a <30cm: desvia usando tração diferencial
    """
    print("\n" + "=" * 60)
    print("🚀 INICIANDO TESTE COMPLETO - Navegação Autônoma")
    print("=" * 60)
    print("⏱️  Duração: 6 segundos")
    print("⚡ Velocidade: Arranque 50% → Controlada 30%")
    print("📏 Regras:")
    print("   • Obstáculo a 70cm: FREIA e espera")
    print("   • Obstáculo a <30cm: DESVIA (tração diferencial)")
    print("=" * 60)
    
    try:
        # Iniciar sensor
        start_sensor()
        time.sleep(0.5)
        
        # Iniciar movimento (arranque 50% → 30%)
        print("\n➡️  Iniciando movimento...")
        print("   (Arranque 50% por 0.3s → 30% controlada)")
        motor_forward(pwm_a, pwm_b, speed=30)
        
        start_time = time.time()
        test_duration = 6  # segundos
        
        while (time.time() - start_time) < test_duration:
            elapsed = time.time() - start_time
            remaining = test_duration - elapsed
            
            # Verificar distância do obstáculo
            dist = current_distance
            
            # SITUAÇÃO 1: Obstáculo muito próximo (<30cm) - DESVIAR
            if dist < 30:
                print(f"\n🚨 OBSTÁCULO MUITO PRÓXIMO! ({dist:.1f}cm)")
                print("🔄 Executando manobra de desvio...")
                
                # Desvio à direita
                print("   → Passo 1: Tração diferencial direita (0.5s)")
                differential_right(pwm_a, pwm_b, speed=50)
                time.sleep(0.5)
                
                print("   → Passo 2: Tração diferencial reversa (0.5s)")
                differential_left(pwm_a, pwm_b, speed=50)
                time.sleep(0.5)
                
                print("   → Passo 3: Voltando à rota normal")
                motor_forward(pwm_a, pwm_b, speed=30)
                
                print("✅ Manobra de desvio concluída!")
            
            # SITUAÇÃO 2: Obstáculo a 70cm - FREAR E ESPERAR
            elif dist < 70:
                print(f"\n⚠️  Obstáculo detectado a {dist:.1f}cm")
                print("🛑 Freando e aguardando obstáculo sair...")
                motor_stop(pwm_a, pwm_b)
                
                # Aguardar até obstáculo sair ou tempo acabar
                wait_start = time.time()
                while current_distance < 70 and (time.time() - start_time) < test_duration:
                    time.sleep(0.1)
                
                # Se obstáculo saiu, continuar
                if current_distance >= 70:
                    print(f"✅ Obstáculo removido! Distância: {current_distance:.1f}cm")
                    print("➡️  Continuando movimento...")
                    motor_forward(pwm_a, pwm_b, speed=30)
            
            # SITUAÇÃO 3: Caminho livre - SEGUIR
            else:
                # Atualizar status a cada segundo
                if int(elapsed) != int(elapsed - 0.1):
                    print(f"🚗 Avançando... (Tempo restante: {remaining:.1f}s | Distância: {dist:.1f}cm)")
            
            time.sleep(0.1)
        
        # Parar motor ao fim do teste
        print("\n⏹️  Tempo de teste esgotado. Parando motor...")
        motor_stop(pwm_a, pwm_b)
        
        # Parar sensor
        stop_sensor()
        
        print("\n✅ TESTE COMPLETO CONCLUÍDO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        motor_stop(pwm_a, pwm_b)
        stop_sensor()

def menu_test_complete(pwm_a, pwm_b):
    """Menu de teste completo"""
    while True:
        print("\n" + "=" * 60)
        print("🚀 PRUEBA COMPLETA")
        print("=" * 60)
        
        response = input("❓ Deseja iniciar o teste completo? (s/n): ").lower().strip()
        
        if response == 's' or response == 'sim':
            test_complete(pwm_a, pwm_b)
            
            # Perguntar se quer repetir
            while True:
                repeat = input("\n❓ Deseja fazer o teste novamente? (s/n): ").lower().strip()
                if repeat == 's' or repeat == 'sim':
                    test_complete(pwm_a, pwm_b)
                elif repeat == 'n' or repeat == 'nao' or repeat == 'não':
                    print("↩️  Voltando ao menu principal...")
                    return
                else:
                    print("❌ Resposta inválida. Digite 's' para sim ou 'n' para não.")
        
        elif response == 'n' or response == 'nao' or response == 'não':
            print("↩️  Voltando ao menu principal...")
            break
        
        else:
            print("❌ Resposta inválida. Digite 's' para sim ou 'n' para não.")

# ============================================================
# MENU PRINCIPAL
# ============================================================

def main_menu():
    """Menu principal do sistema de testes"""
    print("\n" + "=" * 60)
    print("🤖 ARGOS CAR - SISTEMA DE TESTES DEMO")
    print("=" * 60)
    print("Componentes ativos:")
    print("  • Raspberry Pi Zero W")
    print("  • 2x Motores JGA25 12V (L298N)")
    print("  • Sensor HC-SR04 (Detecção de obstáculos)")
    print("=" * 60)
    print("⚡ Modo de Velocidade: Arranque 50% → Controlada 30%")
    print("=" * 60)
    
    # Configurar GPIO e PWM
    pwm_a, pwm_b = setup_gpio()
    
    try:
        while True:
            print("\n" + "=" * 60)
            print("📋 MENU PRINCIPAL")
            print("=" * 60)
            print("1. Prueba de Curva (Teste de tração diferencial)")
            print("2. Prueba Completa (Navegação autônoma)")
            print("3. Sair do sistema")
            print("=" * 60)
            
            choice = input("\n❓ Escolha uma opção (1-3): ").strip()
            
            if choice == '1':
                menu_test_curve(pwm_a, pwm_b)
            
            elif choice == '2':
                menu_test_complete(pwm_a, pwm_b)
            
            elif choice == '3':
                print("\n👋 Encerrando sistema de testes...")
                break
            
            else:
                print("❌ Opção inválida. Escolha 1, 2 ou 3.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Sistema interrompido pelo usuário")
    
    finally:
        cleanup_gpio(pwm_a, pwm_b)
        print("✅ Sistema encerrado com sucesso!")

# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main_menu()

