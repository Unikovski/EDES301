# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Buzzer Music Driver
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
Buzzer Music Driver

Provides note constants and a BuzzerMusic class for playing tones
and songs through a PWM buzzer.

Software API:

  BuzzerMusic(pin)
    play_note(note, length, stop)  - Play a single note
    play_song(song, title, stop)   - Play a song dictionary
    play_song_from_list(index)     - Play song by index from list
    get_song_list_len()            - Return number of songs
    add_song(song)                 - Add a song to the list
    cleanup()                      - Release hardware
--------------------------------------------------------------------------
"""

import time
import buzzer

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

TITLE = "title"
NOTES = "notes"

# ------------------------------------------------------------------------
# Note Library
# ------------------------------------------------------------------------

NOTE_B0  = 31
NOTE_C1  = 33
NOTE_CS1 = 35
NOTE_D1  = 37
NOTE_DS1 = 39
NOTE_E1  = 41
NOTE_F1  = 44
NOTE_FS1 = 46
NOTE_G1  = 49
NOTE_GS1 = 52
NOTE_A1  = 55
NOTE_AS1 = 58
NOTE_B1  = 62
NOTE_C2  = 65
NOTE_CS2 = 69
NOTE_D2  = 73
NOTE_DS2 = 78
NOTE_E2  = 82
NOTE_F2  = 87
NOTE_FS2 = 93
NOTE_G2  = 98
NOTE_GS2 = 104
NOTE_A2  = 110
NOTE_AS2 = 117
NOTE_B2  = 123
NOTE_C3  = 131
NOTE_CS3 = 139
NOTE_D3  = 147
NOTE_DS3 = 156
NOTE_E3  = 165
NOTE_F3  = 175
NOTE_FS3 = 185
NOTE_G3  = 196
NOTE_GS3 = 208
NOTE_A3  = 220
NOTE_AS3 = 233
NOTE_B3  = 247
NOTE_C4  = 262
NOTE_CS4 = 277
NOTE_D4  = 294
NOTE_DS4 = 311
NOTE_E4  = 330
NOTE_F4  = 349
NOTE_FS4 = 370
NOTE_G4  = 392
NOTE_GS4 = 415
NOTE_A4  = 440
NOTE_AS4 = 466
NOTE_B4  = 494
NOTE_C5  = 523
NOTE_CS5 = 554
NOTE_D5  = 587
NOTE_DS5 = 622
NOTE_E5  = 659
NOTE_F5  = 698
NOTE_FS5 = 740
NOTE_G5  = 784
NOTE_GS5 = 831
NOTE_A5  = 880
NOTE_AS5 = 932
NOTE_B5  = 988
NOTE_C6  = 1047
NOTE_CS6 = 1109
NOTE_D6  = 1175
NOTE_DS6 = 1245
NOTE_E6  = 1319
NOTE_F6  = 1397
NOTE_FS6 = 1480
NOTE_G6  = 1568
NOTE_GS6 = 1661
NOTE_A6  = 1760
NOTE_AS6 = 1865
NOTE_B6  = 1976
NOTE_C7  = 2093
NOTE_CS7 = 2217
NOTE_D7  = 2349
NOTE_DS7 = 2489
NOTE_E7  = 2637
NOTE_F7  = 2794
NOTE_FS7 = 2960
NOTE_G7  = 3136
NOTE_GS7 = 3322
NOTE_A7  = 3520
NOTE_AS7 = 3729
NOTE_B7  = 3951
NOTE_C8  = 4186
NOTE_CS8 = 4435
NOTE_D8  = 4699
NOTE_DS8 = 4978

# ------------------------------------------------------------------------
# Song Library
# Each song is a dictionary with:
#   TITLE : string
#   NOTES : list of tuples (frequency, length, stop)
# ------------------------------------------------------------------------

SONGS = [
    {
        "name"  : "Super Mario Theme",
        "notes" : [
            (NOTE_E5, 150), (NOTE_E5, 150), (0, 150), (NOTE_E5, 150),
            (0, 150), (NOTE_C5, 150), (NOTE_E5, 150), (0, 150),
            (NOTE_G5, 150), (0, 450), (NOTE_G4, 150), (0, 450),
            (NOTE_C5, 150), (0, 300), (NOTE_G4, 150), (0, 300),
            (NOTE_E4, 150), (0, 300), (NOTE_A4, 150), (0, 150),
            (NOTE_B4, 150), (0, 150), (NOTE_AS4, 150), (NOTE_A4, 150),
            (0, 150), (NOTE_G4, 100), (NOTE_E5, 100), (NOTE_G5, 100),
            (NOTE_A5, 150), (0, 150), (NOTE_F5, 150), (NOTE_G5, 150),
            (0, 150), (NOTE_E5, 150), (0, 150), (NOTE_C5, 150),
            (NOTE_D5, 150), (NOTE_B4, 150), (0, 300),
        ]
    },
    {
        "name"  : "Tetris Theme",
        "notes" : [
            (NOTE_E5, 150), (NOTE_B4, 75), (NOTE_C5, 75), (NOTE_D5, 150),
            (NOTE_C5, 75), (NOTE_B4, 75), (NOTE_A4, 150), (NOTE_A4, 75),
            (NOTE_C5, 75), (NOTE_E5, 150), (NOTE_D5, 75), (NOTE_C5, 75),
            (NOTE_B4, 225), (NOTE_C5, 75), (NOTE_D5, 150), (NOTE_E5, 150),
            (NOTE_C5, 150), (NOTE_A4, 150), (NOTE_A4, 300),
            (0, 75), (NOTE_D5, 150), (NOTE_F5, 75), (NOTE_A5, 150),
            (NOTE_G5, 75), (NOTE_F5, 75), (NOTE_E5, 225), (NOTE_C5, 75),
            (NOTE_E5, 150), (NOTE_D5, 75), (NOTE_C5, 75), (NOTE_B4, 150),
            (NOTE_B4, 75), (NOTE_C5, 75), (NOTE_D5, 150), (NOTE_E5, 150),
            (NOTE_C5, 150), (NOTE_A4, 150), (NOTE_A4, 300),
        ]
    },
    {
        "name"  : "Happy Birthday",
        "notes" : [
            (NOTE_C5, 150), (NOTE_C5, 75), (NOTE_D5, 225), (NOTE_C5, 225),
            (NOTE_F5, 225), (NOTE_E5, 450), (0, 75),
            (NOTE_C5, 150), (NOTE_C5, 75), (NOTE_D5, 225), (NOTE_C5, 225),
            (NOTE_G5, 225), (NOTE_F5, 450), (0, 75),
            (NOTE_C5, 150), (NOTE_C5, 75), (NOTE_C6, 225), (NOTE_A5, 225),
            (NOTE_F5, 225), (NOTE_E5, 225), (NOTE_D5, 225), (0, 75),
            (NOTE_AS5, 150), (NOTE_AS5, 75), (NOTE_A5, 225), (NOTE_F5, 225),
            (NOTE_G5, 225), (NOTE_F5, 450),
        ]
    },
]

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class BuzzerMusic():
    """ Class to play music through a PWM buzzer """

    buzzer    = None
    song_list = None

    def __init__(self, pin=None, song_list=None):
        """ Initialize the buzzer and song list """

        if pin is None:
            raise ValueError("Pin not provided for BuzzerMusic()")

        self.buzzer = buzzer.Buzzer(pin)
        self.song_list = song_list if song_list is not None else SONGS

    # End def

    def play_note(self, note, length, stop):
        """ Play a single note

        If note is None, rest for the given duration
        """

        if note is None:
            time.sleep(length)
        else:
            self.buzzer.play(note, length, stop)

    # End def

    def play_song(self, song, title=True, stop=True):
        """ Play a song dictionary """

        try:
            if title:
                print(song[TITLE])
        except:
            print("ERROR: Song has no title field")

        try:
            for note in song[NOTES]:
                self.buzzer.play(note[0], note[1], note[2])
        except:
            print("ERROR: Song has no notes field")

        if stop:
            self.buzzer.stop()

    # End def

    def play_song_from_list(self, index, title=True, zero_index=False):
        """ Play a song by index from the song list """

        if not zero_index:
            index = index - 1

        if 0 <= index < len(self.song_list):
            self.play_song(self.song_list[index], title)
        else:
            print("Index out of bounds.")

    # End def

    def get_song_list_len(self):
        """ Return the number of songs in the list """

        return len(self.song_list)

    # End def

    def add_song(self, song):
        """ Add a song to the list """

        self.song_list.append(song)

    # End def

    def cleanup(self):
        """ Release hardware """

        self.buzzer.cleanup()

    # End def

# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    music = BuzzerMusic("P2_1")

    print("Buzzer Music Test")

    try:
        for i in range(music.get_song_list_len()):
            print("Playing song {0}".format(i + 1))
            music.play_song_from_list(i + 1)
    except KeyboardInterrupt:
        pass

    music.cleanup()

    print("Test Complete")