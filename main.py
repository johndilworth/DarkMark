#!/usr/bin/python3
import cwiid
import time
import random
import pi3d
import threading
from pyomxplayer import OMXPlayer
import pygame
from pygame import mixer


pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.fill((0,0,0))
mode = "ambient"

button_delay = 0.6
validation_sec = 5

def connect_wimote():
    try:
        print('Press 1 + 2 on your Wii Remote now ...')
        time.sleep(1)
        wiimote = cwiid.Wiimote()
    except RuntimeError:
        return connect_wimote()

    print('Wii Remote connected...\n')
    wiimote.led = 6
    wiimote.rpt_mode = cwiid.RPT_BTN
    return wiimote

def validate_connection(wiimote):
    try:
        wiimote.request_status()
        return wiimote
    except RuntimeError:
        print("Disconnected - reconnecting")
        wiimote = connect_wimote()
    return wiimote


# play functions for audio files and for videos
def play_wav(file):
    if(mixer.music.get_busy() == 0):
        print(file)
        mixer.music.load(file)
        mixer.music.play()
        mixer.music.set_endevent()

def play_video(file):
    print("playing video")
    player.toggle_pause()

def stop_video():
    player.stop()

# Connect to the Wii Remote. If it times out then quit.
wii = connect_wimote()
time.sleep(1)

for i in range(4):
    wii.rumble = True
    time.sleep(.1)
    wii.rumble = False
    time.sleep(.1)
wii.led = 0
time.sleep(1)

for i in [1, 2, 4, 8, 4, 2, 1, 2, 4, 8, 4, 2, 1, 2, 4, 8, 4, 2, 1, 0]:
    wii.led = i
    time.sleep(.1)
wii.led = 6
wii.rpt_mode = cwiid.RPT_BTN

ambients = ["atmosphere.wav", "lair.wav"]
music = ["darkmark.wav", "voldemort.wav", "maze.wav"]
folly = ['sadtrumbone.wav', 'thunder.wav']

mixer.init()
player = OMXPlayer('videos/stag.mp4', '-o local')

used_sec = 0
done = False

while not done:
    if mode == "ambient":
        if not mixer.music.get_busy():
            play_wav('effects/'+random.choice(ambients))
    if mode == "music":
        if not mixer.music.get_busy():
            play_wav('effects/'+random.choice(music))
    sec = time.localtime(time.time()).tm_sec
    if(sec % validation_sec == 0 and sec != used_sec):
        wii = validate_connection(wii)
        used_sec = sec

    buttons = wii.state['buttons']

    # If Plus and Minus buttons pressed together then rumble and quit.
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print('Closing connection ...')
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        exit(wii)

    # Check if other buttons are pressed by doing a bitwise AND
    if (buttons & cwiid.BTN_LEFT):
        mode = "folly"
        print('Left pressed')
        time.sleep(button_delay)

    if(buttons & cwiid.BTN_RIGHT):
        mode = "folly"
        print('Right pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_UP):
        mode = "music"
        play_wav('effects/'+random.choice(music))
        print('Up pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_DOWN):
        mode = "folly"
        player = OMXPlayer('videos/underpants.mp4', '-o local')
        play_wav('effects/thunder.wav')
        print('Down pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_1):
        mode = "folly"
        play_wav('effects/thunder.wav')
        print('Button 1 pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_2):
        mode = "folly"
        play_wav('effects/sadtrumbone.wav')
        print('Button 2 pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_A):
        mode = "folly"
        player = OMXPlayer('videos/stag.mp4', '-o local')
        print('Button A pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_B):
        mode = "folly"
        player = OMXPlayer('videos/dark-mark.mp4', '-o local')
        print('Button B pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_HOME):
        mode = "ambient"
        play_wav('effects/'+random.choice(ambients))
        print('Home Button pressed')
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_MINUS):
        mode = "none"
        print('Minus Button pressed')
        time.sleep(button_delay)
        # stop any music or video files that might be playing
        mixer.music.fadeout(2000)
        player.stop()

    if (buttons & cwiid.BTN_PLUS):
        print('Plus Button pressed')
        time.sleep(button_delay)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    time.sleep(0.01)

pygame.quit()