#!/bin/bash
# Configure pin modes for Pomodoro Timer project

# I2C pins for HT16K33 display (bus 1)
config-pin P2_09  i2c
config-pin P2_11 i2c

# PWM pin for buzzer
config-pin P2_01  pwm

# ADC pin for potentiometer
# config-pin P1_19 ain

# GPIO pins for buttons (inputs)
config-pin P2_02  gpio
config-pin P2_03  gpio

# GPIO pins for LEDs (outputs)
config-pin P2_04  gpio
config-pin P2_06  gpio
config-pin P2_08  gpio

# GPIO pins for yellow cycle LEDs (outputs)
config-pin P2_27 gpio
config-pin P2_29 gpio
config-pin P2_31 gpio
config-pin P2_33 gpio

echo "Pins configured."