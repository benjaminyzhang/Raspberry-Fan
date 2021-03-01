#!/usr/bin/env python
# encoding: utf-8
# 随温度变化，自动控制风扇转速代码

import RPi.GPIO
import time

RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(2, RPi.GPIO.OUT)
pwm = RPi.GPIO.PWM(2, 100)
RPi.GPIO.setwarnings(False)

# 设置风扇开始关闭温度
start = 40
stop = 27
fan = False

# 定义变量：风扇速度和上次温度
speed = 0
prv_temp = 0

try:
    while True:
        # 读取温度
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            cur = int(f.read()) / 1000

        # 如果温度高于临界值，开开始风扇
        if not fan and cur >= start:
            # 启动时防止风扇卡死先全功率转0.1秒
            if prv_temp < start:
                pwm.start(0)
                pwm.ChangeDutyCycle(100)
                time.sleep(.1)

            # 根据温度调节风扇速率
            speed = min(cur, 100)
            pwm.ChangeDutyCycle(speed)
            fan = True

        # 如果温度小于临界值，开停止风扇
        if fan and cur <= stop:
            pwm.stop()
            fan = False
            prv_temp = cur
        time.sleep(1)
except KeyboardInterrupt:
    pwm.stop()
