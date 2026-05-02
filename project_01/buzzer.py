# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Buzzer Driver
--------------------------------------------------------------------------
License:
Copyright 2025 - Pedro Unikovski

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
Buzzer Driver using PWM

Software API:

  Buzzer(pin)
    play(frequency, length=1.0, stop=False)
      - Play a tone at the given frequency for the given duration
      - frequency : Hz (or None for silence)
      - length    : seconds
      - stop      : if True, stop PWM after playing
    stop(length=0.0)
      - Stop the buzzer
    cleanup()
      - Stop PWM and release hardware
--------------------------------------------------------------------------
"""

import time
import Adafruit_BBIO.PWM as PWM

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Buzzer():
    """ Class to control a PWM buzzer """

    pin = None

    def __init__(self, pin=None):
        """ Initialize the buzzer with the given pin """

        if pin is None:
            raise ValueError("Pin not provided for Buzzer()")

        self.pin = pin

    # End def

    def play(self, frequency, length=1.0, stop=False):
        """ Play a tone at the given frequency for the given duration

        frequency : value in Hz, or None for silence
        length    : duration in seconds
        stop      : stop PWM after playing if True
        """

        if frequency is not None:
            PWM.start(self.pin, 50, frequency)
            time.sleep(length)

        if stop:
            self.stop()

    # End def

    def stop(self, length=0.0):
        """ Stop the buzzer

        length : optional pause after stopping (seconds)
        """

        PWM.stop(self.pin)
        time.sleep(length)

    # End def

    def cleanup(self):
        """ Stop PWM and release hardware """

        PWM.stop(self.pin)
        PWM.cleanup()

    # End def

# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Buzzer Test")

    buzzer = Buzzer("P2_1")

    print("Playing 440 Hz...")
    buzzer.play(440, 1.0, False)
    time.sleep(1.0)

    print("Playing 880 Hz...")
    buzzer.play(880, 1.0, True)
    time.sleep(1.0)

    buzzer.cleanup()

    print("Test Complete")