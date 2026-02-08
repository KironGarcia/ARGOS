#!/usr/bin/env python3
"""
Script de Testes do Sistema de Rodas - ARGOS Car
Testes: Velocidade, Freio de Emergência, Differential Drive
"""

import RPi.GPIO as GPIO
import time

# ==================== CONFIGURAÇÃO DE PINOS ====================
# Pinos do Motor L298N
IN1 = 17  # Physical Pin 11 - Motor A
IN2 = 27  # Physical Pin 13 - Motor A
IN3 = 22  # Physical Pin 15 - Motor B
IN4 = 23  # Physical Pin 16 - Motor B
ENA = 8   # Physical Pin 10 - PWM Motor A (velocidade)
ENB = 18  # Physical Pin 12 - PWM Motor B (velocidade)

# Pinos do Sensor HC-SR04
TRIG_PIN = 24  # Physical Pin 18
ECHO_PIN = 10  # Physical Pin 19

# ==================== CONFIGURAÇÃO INICIAL ====================
def setup_gpio():
    """Configuração inicial dos GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Configurar pinos dos motores
    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    
    # Configurar PWM (frequência 1000 Hz)
    pwm_a = GPIO.PWM(ENA, 1000)
    pwm_b = GPIO.PWM(ENB, 1000)
    pwm_a.start(0)  # Iniciar em 0%
    pwm_b.start(0)
    
    # Configurar pinos do sensor
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Estado inicial: motores parados
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    
    print("✅ GPIO configurado - Sistema pronto")
    return pwm_a, pwm_b

# ==================== FUNÇÕES DE CONTROLE DOS MOTORES ====================
def motor_forward(pwm_a, pwm_b, speed_a, speed_b=None):
    """Motores para frente com velocidade controlada (0-100%)
    Permite velocidades diferentes para cada motor para compensar assimetria"""
    if speed_b is None:
        speed_b = speed_a  # Se não especificado, usa mesma velocidade
    
    GPIO.output(IN1, GPIO.HIGH)  # Motor A frente
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)   # Motor B frente (invertido)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed_a)
    pwm_b.ChangeDutyCycle(speed_b)

def motor_backward(pwm_a, pwm_b, speed_a, speed_b=None):
    """Motores para trás com velocidade controlada (0-100%)
    Permite velocidades diferentes para cada motor para compensar assimetria"""
    if speed_b is None:
        speed_b = speed_a
    
    GPIO.output(IN1, GPIO.LOW)   # Motor A trás
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)  # Motor B trás (invertido)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed_a)
    pwm_b.ChangeDutyCycle(speed_b)

def motor_turn_right(pwm_a, pwm_b, speed):
    """Girar para DIREITA (Motor A trás, Motor B frente)"""
    GPIO.output(IN1, GPIO.LOW)   # Motor A trás
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)   # Motor B frente (invertido)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def motor_turn_left(pwm_a, pwm_b, speed):
    """Girar para ESQUERDA (Motor A frente, Motor B trás)"""
    GPIO.output(IN1, GPIO.HIGH)  # Motor A frente
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)  # Motor B trás (invertido)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def motor_stop(pwm_a, pwm_b):
    """Parar todos os motores INSTANTANEAMENTE"""
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

def instant_brake(pwm_a, pwm_b):
    """Frenagem instantânea (sem gradual)"""
    print("🚨 FREIO INSTANTÂNEO!")
    motor_stop(pwm_a, pwm_b)
    print("⏹️  PARADO")

# ==================== FUNÇÕES DO SENSOR ====================
def measure_distance():
    """Medir distância com sensor HC-SR04"""
    try:
        # Enviar pulso de disparo
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microsegundos
        GPIO.output(TRIG_PIN, GPIO.LOW)
        
        # Medir tempo do pulso ECHO (com timeout)
        timeout = time.time() + 0.1  # 100ms timeout
        
        pulse_start = time.time()
        while GPIO.input(ECHO_PIN) == GPIO.LOW:
            pulse_start = time.time()
            if pulse_start > timeout:
                return 999  # Distância inválida
        
        pulse_end = time.time()
        while GPIO.input(ECHO_PIN) == GPIO.HIGH:
            pulse_end = time.time()
            if pulse_end > timeout:
                return 999  # Distância inválida
        
        # Calcular distância
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2
        
        return round(distance, 2)
    except:
        return 999  # Em caso de erro, retornar valor seguro

# ==================== TESTE 1: CALIBRAÇÃO DE VELOCIDADE ====================
def test_speed_calibration(pwm_a, pwm_b):
    """Teste de velocidade com calibração assimétrica para compensar delay do Motor B"""
    print("\n" + "="*60)
    print("🎯 TESTE 1: CALIBRAÇÃO DE VELOCIDADE (ASSIMÉTRICA)")
    print("="*60)
    print("📋 Sequência:")
    print("   Motor A: 20% → 40% (frente e trás)")
    print("   Motor B: 30% → 50% (compensação de delay)")
    print("   Duração: 4 segundos cada direção")
    print("="*60)
    
    input("\n🎬 Pressione ENTER para iniciar o teste...")
    
    try:
        # FASE 1: FRENTE (Motor A: 20→40%, Motor B: 30→50%)
        print("\n🚗 FASE 1: ACELERANDO PARA FRENTE...")
        print("   Motor A: 20% → 40%")
        print("   Motor B: 30% → 50% (compensação)")
        
        duration = 4.0  # 4 segundos
        steps = 40  # 40 steps = 100ms por step
        min_speed_a = 20
        max_speed_a = 40
        min_speed_b = 30
        max_speed_b = 50
        
        for i in range(steps + 1):
            # Calcular velocidade progressiva para cada motor
            progress = i / steps
            speed_a = min_speed_a + (max_speed_a - min_speed_a) * progress
            speed_b = min_speed_b + (max_speed_b - min_speed_b) * progress
            
            motor_forward(pwm_a, pwm_b, speed_a, speed_b)
            
            # Mostrar progresso a cada 10 steps
            if i % 10 == 0:
                print(f"   ➡️  Motor A: {speed_a:.0f}% | Motor B: {speed_b:.0f}%")
            
            time.sleep(duration / steps)
        
        # FASE 2: PARAR
        print("\n⏸️  FASE 2: PARANDO (1 segundo)...")
        motor_stop(pwm_a, pwm_b)
        time.sleep(1)
        
        # FASE 3: TRÁS (Motor A: 20→40%, Motor B: 30→50%)
        print("\n🔄 FASE 3: ACELERANDO PARA TRÁS...")
        print("   Motor A: 20% → 40%")
        print("   Motor B: 30% → 50% (compensação)")
        
        for i in range(steps + 1):
            # Calcular velocidade progressiva para cada motor
            progress = i / steps
            speed_a = min_speed_a + (max_speed_a - min_speed_a) * progress
            speed_b = min_speed_b + (max_speed_b - min_speed_b) * progress
            
            motor_backward(pwm_a, pwm_b, speed_a, speed_b)
            
            # Mostrar progresso a cada 10 steps
            if i % 10 == 0:
                print(f"   ⬅️  Motor A: {speed_a:.0f}% | Motor B: {speed_b:.0f}%")
            
            time.sleep(duration / steps)
        
        # FASE 4: PARAR FINAL
        print("\n⏹️  FASE 4: PARADA FINAL")
        motor_stop(pwm_a, pwm_b)
        
        print("\n✅ TESTE DE VELOCIDADE COMPLETADO!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        motor_stop(pwm_a, pwm_b)

# ==================== TESTE 2: FREIO DE EMERGÊNCIA ====================
def test_emergency_brake(pwm_a, pwm_b):
    """Teste do sistema de freio com sensor ultrassônico"""
    print("\n" + "="*60)
    print("🚨 TESTE 2: FREIO DE EMERGÊNCIA")
    print("="*60)
    print("📋 Descrição:")
    print("   • Velocidade: 30% → 50%")
    print("   • Duração: 15 segundos")
    print("   • Se obstáculo < 30cm: FREIO INSTANTÂNEO")
    print("   • Se obstáculo sai: VOLTA A ANDAR")
    print("   • Pode repetir várias vezes durante o teste!")
    print("="*60)
    
    while True:
        input("\n🎬 Pressione ENTER para iniciar o teste...")
        
        try:
            duration = 15.0  # 15 segundos
            min_speed = 30
            max_speed = 50
            start_time = time.time()
            current_speed_a = min_speed
            current_speed_b = min_speed
            is_stopped = False
            last_status_print = time.time()
            
            print("\n🚗 INICIANDO TESTE...")
            print("   Velocidade máxima: 50%")
            print("   Monitorando obstáculos continuamente...\n")
            
            while time.time() - start_time < duration:
                # Verificar distância do obstáculo
                distance = measure_distance()
                
                # LÓGICA: Obstáculo < 30cm → PARA | Obstáculo > 30cm → ANDA
                if distance < 30:
                    # OBSTÁCULO DETECTADO - PARAR CARRO INSTANTANEAMENTE
                    if not is_stopped:
                        print(f"\n🚨 OBSTÁCULO DETECTADO! Distância: {distance:.1f}cm")
                        instant_brake(pwm_a, pwm_b)
                        is_stopped = True
                    else:
                        # Já está parado, apenas manter parado
                        motor_stop(pwm_a, pwm_b)
                        # Mostrar status a cada 0.5 segundos
                        if time.time() - last_status_print > 0.5:
                            print(f"⏸️  PARADO - Aguardando obstáculo sair... (Dist: {distance:.1f}cm)")
                            last_status_print = time.time()
                
                else:
                    # CAMINHO LIVRE - ANDAR
                    if is_stopped:
                        print(f"\n✅ CAMINHO LIVRE! Distância: {distance:.1f}cm")
                        print("🚗 VOLTANDO A ANDAR...")
                        is_stopped = False
                    
                    # Calcular velocidade progressiva baseada no tempo decorrido
                    elapsed = time.time() - start_time
                    progress = min(elapsed / (duration * 0.5), 1.0)  # Chega ao máximo em 7.5s
                    current_speed_a = min_speed + (max_speed - min_speed) * progress
                    current_speed_b = min_speed + (max_speed - min_speed) * progress
                    
                    motor_forward(pwm_a, pwm_b, current_speed_a, current_speed_b)
                    
                    # Mostrar progresso a cada 0.5 segundos
                    if time.time() - last_status_print > 0.5:
                        print(f"   ➡️  Velocidade: {current_speed_a:.0f}% | Distância: {distance:.1f}cm")
                        last_status_print = time.time()
                
                time.sleep(0.1)  # Verificar a cada 100ms
            
            # Tempo esgotado
            print("\n⏱️  TEMPO ESGOTADO (15 segundos)")
            motor_stop(pwm_a, pwm_b)
            
            print("\n✅ TESTE DE FREIO COMPLETADO!")
            print("="*60)
            
            # Perguntar se quer repetir
            response = input("\n❓ Deseja executar a prova de novo? (s/n): ").lower().strip()
            if response in ['n', 'nao', 'não', 'no']:
                print("↩️  Voltando ao menu principal...")
                break
            else:
                print("\n🔄 Repetindo teste...")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Teste interrompido pelo usuário")
            motor_stop(pwm_a, pwm_b)
            break

# ==================== TESTE 3: DIFFERENTIAL DRIVE ====================
def test_differential_drive(pwm_a, pwm_b):
    """Teste de giro estático usando tração diferencial"""
    print("\n" + "="*60)
    print("🔄 TESTE 3: DIFFERENTIAL DRIVE (GIROS ESTÁTICOS)")
    print("="*60)
    print("📋 Descrição:")
    print("   • Giro no próprio eixo (sem avançar)")
    print("   • Esquerda: Motor A frente + Motor B trás")
    print("   • Direita: Motor A trás + Motor B frente")
    print("   • Velocidade de giro: 50%")
    print("   • Duração do giro: 0.5 segundos (meio segundo)")
    print("="*60)
    
    turn_speed = 50  # Velocidade base para giros
    turn_duration = 0.5  # 0.5 segundos de giro (meio segundo)
    
    while True:
        print("\n🎯 ESCOLHA A DIREÇÃO DO GIRO:")
        print("   1. Girar para ESQUERDA ⬅️")
        print("   2. Girar para DIREITA ➡️")
        print("   3. Voltar ao menu principal")
        
        choice = input("\n❓ Digite sua escolha (1/2/3): ").strip()
        
        if choice == '1':
            # GIRO PARA ESQUERDA
            print("\n⬅️  GIRANDO PARA ESQUERDA...")
            print(f"   Velocidade: {turn_speed}%")
            print(f"   Duração: {turn_duration} segundos")
            
            try:
                input("\n🎬 Pressione ENTER para executar o giro...")
                
                print("\n🔄 EXECUTANDO GIRO À ESQUERDA...")
                motor_turn_left(pwm_a, pwm_b, turn_speed)
                
                # Mostrar progresso
                for i in range(int(turn_duration * 4)):  # 4 updates por segundo
                    time.sleep(0.25)
                    print("   ↺ Girando...", end="\r")
                
                motor_stop(pwm_a, pwm_b)
                print("\n✅ GIRO À ESQUERDA COMPLETO!")
                
            except KeyboardInterrupt:
                print("\n⚠️  Giro interrompido")
                motor_stop(pwm_a, pwm_b)
        
        elif choice == '2':
            # GIRO PARA DIREITA
            print("\n➡️  GIRANDO PARA DIREITA...")
            print(f"   Velocidade: {turn_speed}%")
            print(f"   Duração: {turn_duration} segundos")
            
            try:
                input("\n🎬 Pressione ENTER para executar o giro...")
                
                print("\n🔄 EXECUTANDO GIRO À DIREITA...")
                motor_turn_right(pwm_a, pwm_b, turn_speed)
                
                # Mostrar progresso
                for i in range(int(turn_duration * 4)):  # 4 updates por segundo
                    time.sleep(0.25)
                    print("   ↻ Girando...", end="\r")
                
                motor_stop(pwm_a, pwm_b)
                print("\n✅ GIRO À DIREITA COMPLETO!")
                
            except KeyboardInterrupt:
                print("\n⚠️  Giro interrompido")
                motor_stop(pwm_a, pwm_b)
        
        elif choice == '3':
            print("\n↩️  Voltando ao menu principal...")
            break
        
        else:
            print("\n❌ Opção inválida! Digite 1, 2 ou 3.")

# ==================== MENU PRINCIPAL ====================
def show_menu():
    """Mostrar menu principal"""
    print("\n" + "="*60)
    print("🚗 MENU PRINCIPAL - TESTES DO SISTEMA DE RODAS")
    print("="*60)
    print("1. 🎯 Teste de Calibração Assimétrica (A: 20→40%, B: 30→50%)")
    print("2. 🚨 Teste de Freio Instantâneo (30→50%, sensor 30cm)")
    print("3. 🔄 Teste de Differential Drive (50%, 0.5s)")
    print("4. 🚪 Sair do sistema")
    print("="*60)

def main():
    """Função principal"""
    print("🤖 SISTEMA DE TESTES - ARGOS CAR")
    print("="*60)
    print("Componentes ativos:")
    print("• Raspberry Pi Zero W")
    print("• 2x Motores JGA25 12V (L298N)")
    print("• Sensor HC-SR04 (Ultrassônico)")
    print("• Sistema PWM para controle de velocidade")
    print("="*60)
    
    # Configurar GPIO
    pwm_a, pwm_b = setup_gpio()
    
    try:
        while True:
            show_menu()
            choice = input("\n❓ Digite sua escolha (1/2/3/4): ").strip()
            
            if choice == '1':
                test_speed_calibration(pwm_a, pwm_b)
            
            elif choice == '2':
                test_emergency_brake(pwm_a, pwm_b)
            
            elif choice == '3':
                test_differential_drive(pwm_a, pwm_b)
            
            elif choice == '4':
                print("\n👋 Encerrando sistema...")
                break
            
            else:
                print("\n❌ Opção inválida! Digite um número de 1 a 4.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Sistema interrompido pelo usuário")
    
    finally:
        # Limpeza final
        motor_stop(pwm_a, pwm_b)
        pwm_a.stop()
        pwm_b.stop()
        GPIO.cleanup()
        print("🔧 GPIO limpo")
        print("✅ Sistema encerrado com sucesso!")

if __name__ == "__main__":
    main()

