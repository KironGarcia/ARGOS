#!/usr/bin/env python3
"""
LED Demo for Raspberry Pi Zero
Demonstrates different LED lighting patterns
"""

import RPi.GPIO as GPIO
import time

# LED pin assignments (change these to match your wiring)
LED_PINS = [17, 27, 22, 23, 18, 10]  # GPIO pins for LEDs

#LED_PINS = [27, 22,10]

def setup():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setwarnings(False)  # Disable warnings
    
    # Set all LED pins as outputs
    for pin in LED_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Start with all LEDs off

def cleanup():
    """Clean up GPIO settings"""
    GPIO.cleanup()

def all_on():
    """Turn all LEDs on"""
    print("All LEDs ON")
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.HIGH)

def all_off():
    """Turn all LEDs off"""
    print("All LEDs OFF")
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.LOW)

def blink_all(times=3, delay=0.5):
    """Blink all LEDs together"""
    print(f"Blinking all LEDs {times} times")
    for _ in range(times):
        all_on()
        time.sleep(delay)
        all_off()
        time.sleep(delay)

def chase_pattern(cycles=2, delay=0.2):
    """Create a chase/running light pattern"""
    print(f"Running chase pattern {cycles} times")
    for _ in range(cycles):
        for pin in LED_PINS:
            all_off()
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(delay)

def wave_pattern(cycles=2, delay=0.1):
    """Create a wave pattern (on then off in sequence)"""
    print(f"Running wave pattern {cycles} times")
    for _ in range(cycles):
        # Forward wave
        for pin in LED_PINS:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(delay)
        # Backward wave (turn off)
        for pin in reversed(LED_PINS):
            GPIO.output(pin, GPIO.LOW)
            time.sleep(delay)

def binary_counter(max_count=8, delay=1):
    """Display binary counting on LEDs"""
    print(f"Binary counter from 0 to {max_count-1}")
    for count in range(max_count):
        all_off()
        # Convert number to binary and light corresponding LEDs
        for i, pin in enumerate(LED_PINS[:3]):  # Use first 3 LEDs for 3-bit binary
            if count & (1 << i):
                GPIO.output(pin, GPIO.HIGH)
        print(f"Count: {count}, Binary: {bin(count)[2:].zfill(3)}")
        time.sleep(delay)

def random_blink(duration=5):
    """Random LED blinking"""
    import random
    print(f"Random blinking for {duration} seconds")
    start_time = time.time()
    
    while time.time() - start_time < duration:
        all_off()
        # Turn on random LEDs
        num_leds = random.randint(1, len(LED_PINS))
        selected_pins = random.sample(LED_PINS, num_leds)
        for pin in selected_pins:
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.3)

def breathing_effect(cycles=3):
    """Simulate breathing effect using PWM"""
    print(f"Breathing effect {cycles} times")
    
    # Set up PWM on all pins
    pwm_objects = []
    for pin in LED_PINS:
        pwm = GPIO.PWM(pin, 100)  # 100 Hz frequency
        pwm.start(0)  # Start with 0% duty cycle (off)
        pwm_objects.append(pwm)
    
    try:
        for _ in range(cycles):
            # Fade in
            for duty_cycle in range(0, 101, 2):
                for pwm in pwm_objects:
                    pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.03)
            
            # Fade out
            for duty_cycle in range(100, -1, -2):
                for pwm in pwm_objects:
                    pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.03)
    finally:
        # Clean up PWM objects
        for pwm in pwm_objects:
            pwm.stop()

def main():
    """Main demo function"""
    print("🌟 Raspberry Pi Zero LED Demo 🌟")
    print(f"Using GPIO pins: {LED_PINS}")
    print("Wire LEDs with resistors between GPIO pins and GND")
    print("\nPress Ctrl+C to exit\n")
    
    setup()
    
    try:
        while True:
            print("\n" + "="*40)

            
            # Demo sequence
            blink_all(3, 0.5)
            time.sleep(1)
            
            chase_pattern(2, 0.15)
            time.sleep(1)
            
            wave_pattern(2, 0.1)
            time.sleep(1)
            
            binary_counter(8, 0.8)
            time.sleep(1)
            
            random_blink(3)
            time.sleep(1)
            
            breathing_effect(2)
            time.sleep(1)
            
            print("\n🔄 Repeating demo... (Ctrl+C to exit)")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n👋 Exiting LED demo...")
    finally:
        all_off()
        cleanup()
        print("GPIO cleaned up. Goodbye!")

if __name__ == "__main__":
    main()

