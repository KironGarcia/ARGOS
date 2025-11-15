#!/usr/bin/env python3
"""
Sistema Principal do Carro Inteligente
Integração de sensores HC-SR04 e controle de motores L298N
"""

import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime

# Configuração dos pinos do sensor HC-SR04
TRIG_PIN = 24  # Physical Pin 18
ECHO_PIN = 10  # Physical Pin 19

# Configuração dos pinos do motor L298N
IN1 = 17  # Physical Pin 11 - Motor A
IN2 = 27  # Physical Pin 13 - Motor A  
IN3 = 22  # Physical Pin 15 - Motor B
IN4 = 23  # Physical Pin 16 - Motor B

# Variáveis de controle do sistema
obstacle_detected = False
system_running = False
sensor_running = False
motor_thread = None
sensor_thread = None
distance = 0
obstacle_start_time = None

def setup_gpio():
    """Configuração inicial dos GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Configurar pinos do sensor
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Configurar pinos dos motores
    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    
    print("✅ GPIO configurado - Sistema pronto")

def measure_distance():
    """Medir distância com sensor HC-SR04"""
    global distance
    
    # Enviar pulso de disparo
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microsegundos
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Medir tempo do pulso ECHO
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    
    # Calcular distância
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2
    
    return round(distance, 2)

def sensor_monitor():
    """Thread para monitoramento contínuo do sensor"""
    global obstacle_detected, sensor_running, obstacle_start_time
    
    while sensor_running:
        try:
            current_distance = measure_distance()
            
            # Verificar obstáculo (distância < 30cm)
            if current_distance < 30:
                if not obstacle_detected:
                    obstacle_detected = True
                    obstacle_start_time = time.time()
                    print("🚨 OBSTÁCULO DETECTADO! Parando motores...")
            else:
                if obstacle_detected:
                    obstacle_detected = False
                    obstacle_start_time = None
                    print("✅ CAMINHO LIVRE! Continuando movimento...")
            
            time.sleep(0.1)  # Verificar a cada 100ms
            
        except Exception as e:
            print(f"❌ Erro no sensor: {e}")
            time.sleep(0.5)

def motor_forward():
    """Motores para frente"""
    GPIO.output(IN1, GPIO.HIGH)  # Motor A frente
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)   # Motor B frente (invertido)
    GPIO.output(IN4, GPIO.HIGH)

def motor_backward():
    """Motores para trás"""
    GPIO.output(IN1, GPIO.LOW)   # Motor A trás
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)  # Motor B trás (invertido)
    GPIO.output(IN4, GPIO.LOW)

def motor_stop():
    """Parar todos os motores"""
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

def ask_user_reverse():
    """Perguntar ao usuário se quer retroceder"""
    try:
        response = input("❓ Obstáculo persistente. Deseja retroceder? (s/n): ").lower().strip()
        return response == 's' or response == 'sim'
    except:
        return False

def motor_control():
    """Thread principal de controle dos motores"""
    global system_running, obstacle_detected, obstacle_start_time
    
    print("🚗 Iniciando sequência de movimento dos motores...")
    
    while system_running:
        try:
            if not obstacle_detected:
                # Movimento normal: 8s frente, 8s trás
                print("➡️  Movendo para FRENTE por 8 segundos...")
                motor_forward()
                
                # Verificar obstáculos durante movimento para frente
                for i in range(80):  # 8 segundos = 80 x 0.1s
                    if obstacle_detected:
                        motor_stop()
                        print("⏸️  Movimento interrompido por obstáculo")
                        break
                    time.sleep(0.1)
                
                if not obstacle_detected and system_running:
                    motor_stop()
                    time.sleep(1)  # Pausa entre movimentos
                    
                    print("⬅️  Movendo para TRÁS por 8 segundos...")
                    motor_backward()
                    
                    # Verificar obstáculos durante movimento para trás
                    for i in range(80):  # 8 segundos = 80 x 0.1s
                        if obstacle_detected:
                            motor_stop()
                            print("⏸️  Movimento interrompido por obstáculo")
                            break
                        time.sleep(0.1)
                    
                    if not obstacle_detected and system_running:
                        motor_stop()
                        time.sleep(1)  # Pausa entre ciclos
            
            else:
                # Obstáculo detectado - parar e aguardar
                motor_stop()
                
                if obstacle_start_time:
                    elapsed_time = time.time() - obstacle_start_time
                    
                    # Se obstáculo persiste por mais de 1 minuto
                    if elapsed_time > 60:
                        if ask_user_reverse():
                            print("⬅️  Retrocedendo por 5 segundos...")
                            motor_backward()
                            time.sleep(5)
                            motor_stop()
                        
                        # Reset do timer
                        obstacle_start_time = time.time()
                    
                    # Se obstáculo desaparece em menos de 1 minuto
                    elif not obstacle_detected:
                        print("➡️  Obstáculo removido! Avançando 5 segundos...")
                        motor_forward()
                        time.sleep(5)
                        motor_stop()
                        time.sleep(1)
                        
                        print("⬅️  Retrocedendo por 8 segundos...")
                        motor_backward()
                        time.sleep(8)
                        motor_stop()
                
                time.sleep(0.5)  # Verificar obstáculos a cada 500ms
                
        except Exception as e:
            print(f"❌ Erro no controle dos motores: {e}")
            motor_stop()
            time.sleep(1)

def start_presentation():
    """Iniciar apresentação do sistema"""
    global system_running, sensor_running, motor_thread, sensor_thread
    
    print("\n🎬 INICIANDO APRESENTAÇÃO DO CARRO INTELIGENTE")
    print("=" * 60)
    
    # Inicializar GPIO
    setup_gpio()
    
    # Iniciar sensor
    print("\n📡 Iniciando sistema de sensores...")
    sensor_running = True
    sensor_thread = threading.Thread(target=sensor_monitor, daemon=True)
    sensor_thread.start()
    time.sleep(2)
    print("✅ Sensor ligado e pronto para detectar obstáculos!")
    
    # Iniciar motores
    print("\n🔧 Iniciando sistema de motores...")
    system_running = True
    motor_thread = threading.Thread(target=motor_control, daemon=True)
    motor_thread.start()
    time.sleep(1)
    print("✅ Motores ligados e prontos para movimento!")
    
    print("\n🚀 SISTEMA TOTALMENTE OPERACIONAL!")
    print("📋 Status:")
    print("   • Sensores: ATIVO")
    print("   • Motores: ATIVO") 
    print("   • Detecção de obstáculos: ATIVA")
    print("\n⚠️  Pressione Ctrl+C para parar o sistema")

def stop_system():
    """Parar todo o sistema"""
    global system_running, sensor_running
    
    print("\n🛑 Parando sistema...")
    system_running = False
    sensor_running = False
    
    motor_stop()
    time.sleep(1)
    
    GPIO.cleanup()
    print("🔧 GPIO limpo")
    print("👋 Sistema encerrado com sucesso!")

def main():
    """Função principal"""
    print("🤖 SISTEMA DO CARRO INTELIGENTE")
    print("=" * 50)
    print("Componentes:")
    print("• Raspberry Pi Zero W")
    print("• Sensor HC-SR04 (Detecção de obstáculos)")
    print("• Controlador L298N (Motores)")
    print("• 2x Motores DC")
    print("=" * 50)
    
    try:
        while True:
            print(f"\n🕐 {datetime.now().strftime('%H:%M:%S')}")
            response = input("❓ Deseja iniciar a apresentação? (s/n): ").lower().strip()
            
            if response == 's' or response == 'sim':
                start_presentation()
                
                # Manter sistema rodando até Ctrl+C
                try:
                    while system_running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    stop_system()
                    break
                    
            elif response == 'n' or response == 'nao' or response == 'não':
                print("👋 Saindo do sistema...")
                break
            else:
                print("❌ Resposta inválida. Digite 's' para sim ou 'n' para não.")
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Sistema interrompido pelo usuário")
        if system_running:
            stop_system()

if __name__ == "__main__":
    main() 