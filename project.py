import machine as m
import utime as u

# Ultrasonic pins
l=m.Pin(25,m.Pin.OUT)
l.on()
t1 = m.Pin(0, m.Pin.OUT)
e1 = m.Pin(1, m.Pin.IN)

t2 = m.Pin(4, m.Pin.OUT)
e2 = m.Pin(5, m.Pin.IN)

# Servo pin (PWM)
servo = m.PWM(m.Pin(15))
servo.freq(50)   # 50 Hz for servo

def set_servo(angle):
    # angle: 0–180
    duty = int(1638 + (angle / 180) * 819)  
    servo.duty_u16(duty)

def measure_distance(trig, echo):
    trig.low()
    u.sleep_us(2)
    trig.high()
    u.sleep_us(10)
    trig.low()

    timeout = 30000

    start = u.ticks_us()
    while echo.value() == 0:
        if u.ticks_diff(u.ticks_us(), start) > timeout:
            return -1
    signal_on = u.ticks_us()

    while echo.value() == 1:
        if u.ticks_diff(u.ticks_us(), signal_on) > timeout:
            return -1
    signal_off = u.ticks_us()

    time_passed = u.ticks_diff(signal_off, signal_on)
    return (time_passed * 0.0343) / 2

# Initial position
set_servo(0)

while True:
    d1 = measure_distance(t1, e1)
    u.sleep_ms(60)
    d2 = measure_distance(t2, e2)

    print("D1:", d1, "cm", "D2:", d2, "cm")

    if (d1 != -10 or d2 != -10) and (d1 <= 10 or d2 <= 10):
        set_servo(0)   # ON
        print("Servo ON")
    else:
        set_servo(720)    # OFF
        print("Servo OFF")

    u.sleep(0.3)


