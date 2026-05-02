# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
LED Driver
--------------------------------------------------------------------------
License:
Copyright 2025 - Pedro Cardon Unikovski

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
LED Driver

Uses "active_high" flag to determine LED polarity:
  active_high=True  --> HIGH turns LED on, LOW turns it off
  active_high=False --> LOW turns LED on, HIGH turns it off

Software API:

  LED(pin, active_high=True)
    on()       - Turn the LED on
    off()      - Turn the LED off
    is_on()    - Returns True if LED is on, False otherwise
    cleanup()  - Turn off LED and release hardware
--------------------------------------------------------------------------
"""

import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

HIGH = GPIO.HIGH
LOW  = GPIO.LOW

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class LED():
    """ Class to control an LED via GPIO """

    pin       = None
    on_value  = None
    off_value = None

    def __init__(self, pin=None, active_high=True):
        """ Initialize variables and configure the LED pin """

        if pin is None:
            raise ValueError("Pin not provided for LED()")

        self.pin = pin

        if active_high:
            self.on_value  = HIGH
            self.off_value = LOW
        else:
            self.on_value  = LOW
            self.off_value = HIGH

        self._setup()

    # End def

    def _setup(self):
        """ Configure the GPIO pin as output and default to off """

        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    # End def

    def is_on(self):
        """ Returns True if the LED is currently on """

        return GPIO.input(self.pin) == self.on_value

    # End def

    def on(self):
        """ Turn the LED on """

        GPIO.output(self.pin, self.on_value)

    # End def

    def off(self):
        """ Turn the LED off """

        GPIO.output(self.pin, self.off_value)

    # End def

    def cleanup(self):
        """ Turn off LED and release hardware """

        self.off()

    # End def

# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    import time

    print("LED Test")

    led = LED("P2_4")

    print("Use Ctrl-C to exit")

    try:
        while True:
            led.on()
            print("LED on: {0}".format(led.is_on()))
            time.sleep(1)

            led.off()
            print("LED on: {0}".format(led.is_on()))
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    print("Test Complete")