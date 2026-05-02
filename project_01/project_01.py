# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Pomodoro Timer - Project 01
--------------------------------------------------------------------------
License:
Copyright 2025 Pedro Cardon Unikovski

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from this
software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Pomodoro Timer:
  - Potentiometer sets study duration (15-45 minutes)
  - 4 study cycles with short breaks (5 min) between them
  - Long break (10 min) after completing all 4 cycles
  - Green button starts/pauses the timer
  - Blue button resets the timer
  - Yellow LEDs indicate current cycle (1-4)
  - Blue LED = studying, Red LED = on break
  - White LED = timer running
  - HT16K33 display shows time remaining (MM:SS)
  - Buzzer plays a song when a session ends

--------------------------------------------------------------------------
"""
import time
import sys

import Adafruit_BBIO.GPIO as GPIO

from ht16k33       import HT16K33
from led           import LED
from button        import Button
from potentiometer import Potentiometer
from buzzer_music  import BuzzerMusic

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

DISPLAY_BUS     = 1
DISPLAY_ADDR    = 0x70

PIN_BTN_GREEN   = "P2_3"
PIN_BTN_BLUE    = "P2_2"

PIN_LED_BLUE    = "P2_4"
PIN_LED_RED     = "P2_6"
PIN_LED_WHITE   = "P2_8"
PIN_LED_YELLOW  = ["P2_27", "P2_29", "P2_31", "P2_33"]

PIN_POT         = "P1_19"
PIN_BUZZER      = "P2_1"

NUM_CYCLES      = 4
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN  = 10
MIN_STUDY_MIN   = 15
MAX_STUDY_MIN   = 45
ADC_MAX         = 4095

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

display     = None
btn_green   = None
btn_blue    = None
led_blue    = None
led_red     = None
led_white   = None
leds_yellow = []
pot         = None
music       = None

# ------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------

def setup():
    """Initialize all hardware components."""
    global display, btn_green, btn_blue
    global led_blue, led_red, led_white, leds_yellow
    global pot, music

    display   = HT16K33(DISPLAY_BUS, DISPLAY_ADDR)
    btn_green = Button(PIN_BTN_GREEN)
    btn_blue  = Button(PIN_BTN_BLUE)
    led_blue  = LED(PIN_LED_BLUE)
    led_red   = LED(PIN_LED_RED)
    led_white = LED(PIN_LED_WHITE)

    for pin in PIN_LED_YELLOW:
        leds_yellow.append(LED(pin))

    pot   = Potentiometer(PIN_POT)
    music = BuzzerMusic(PIN_BUZZER)

# End def


def cleanup():
    """Turn off all outputs and clean up GPIO."""
    display.blank()
    led_blue.cleanup()
    led_red.cleanup()
    led_white.cleanup()
    for led in leds_yellow:
        led.cleanup()
    music.cleanup()
    GPIO.cleanup()

# End def


def read_study_duration():
    """Read potentiometer and map to study duration in minutes (15-45)."""
    raw      = pot.get_value()
    duration = MIN_STUDY_MIN + int((raw / ADC_MAX) * (MAX_STUDY_MIN - MIN_STUDY_MIN))
    return duration

# End def


def show_cycle_leds(cycle_num):
    """Light yellow LEDs to indicate current cycle (1-4)."""
    for i, led in enumerate(leds_yellow):
        if i < cycle_num:
            led.on()
        else:
            led.off()

# End def


def update_display(seconds_remaining):
    """Show MM:SS on the 7-segment display."""
    mins  = seconds_remaining // 60
    secs  = seconds_remaining % 60
    value = mins * 100 + secs
    display.update(value)
    display.set_colon(True)

# End def


def run_timer(duration_sec, is_break=False):
    """
    Count down duration_sec seconds.
    Green button pauses/resumes. Blue button returns False (reset requested).
    Returns True when timer completes normally, False if reset requested.
    """
    if is_break:
        led_red.on()
        led_blue.off()
    else:
        led_blue.on()
        led_red.off()

    led_white.on()
    remaining = duration_sec

    while remaining > 0:
        update_display(remaining)

        if btn_blue.is_pressed():
            return False

        if btn_green.is_pressed():
            led_white.off()
            time.sleep(1)
            btn_green.wait_for_press()
            led_white.on()

        time.sleep(1)
        remaining -= 1

    led_white.off()
    return True

# End def


def pomodoro_loop():
    """Main Pomodoro loop."""
    print("Pomodoro Timer ready. Press green button to start.")
    display.text("rdy ")

    btn_green.wait_for_press()

    while True:
        study_min = read_study_duration()
        print("Study duration: {0} min".format(study_min))

        for cycle in range(1, NUM_CYCLES + 1):
            show_cycle_leds(cycle)
            print("Cycle {0} - Study for {1} min".format(cycle, study_min))
            display.text("Stdy")
            time.sleep(1)

            completed = run_timer(study_min * 60, is_break=False)
            if not completed:
                print("Reset requested.")
                return

            music.play_song(0)

            if cycle < NUM_CYCLES:
                break_min = SHORT_BREAK_MIN
                print("Short break: {0} min".format(break_min))
                display.text("bRK ")
            else:
                break_min = LONG_BREAK_MIN
                print("Long break: {0} min".format(break_min))
                display.text("LBRK")

            time.sleep(1)
            completed = run_timer(break_min * 60, is_break=True)
            if not completed:
                print("Reset requested.")
                return

            music.play_song(1)

        show_cycle_leds(0)
        display.text("done")
        print("All cycles complete!")
        music.play_song(2)
        time.sleep(3)

        print("Press green button to start again.")
        display.text("rdy ")
        btn_green.wait_for_press()
        study_min = read_study_duration()

# End def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == "__main__":
    setup()

    try:
        pomodoro_loop()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        cleanup()