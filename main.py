#!/usr/bin/python
import cwiid
import time
import random
import threading
from pyomxplayer import OMXPlayer

from pygame import mixer

validation_sec = 5

# Connect to the Wii Remote. If it times out
# then quit.

def connect_wimote():
	try:
		print 'Press 1 + 2 on your Wii Remote now ...'
		time.sleep(1)
  		wiimote = cwiid.Wiimote()
	except RuntimeError:
		return connect_wimote()

	print 'Wii Remote connected...\n'
	wiimote.led = 6
	wiimote.rpt_mode = cwiid.RPT_BTN
	return wiimote

def validate_connection(wiimote):
	try:
		wiimote.request_status()
		return wiimote
	except RuntimeError:
		print "Disconnected - reconnecting"
		wiimote = connect_wimote()
	return wiimote

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

player = OMXPlayer('videos/dark-mark.mp4', '-o local', start_playback=False)
player.toggle_pause()
mixer.init()
prefix = "videos/"
effects_prefix = "effects/"
videos = ["stag.mp4","dark-mark.mp4"]
effects = ["ambient1.wav", "ambient2.wav", "ambient3.wav"]
used_sec = 0

while True:
  sec = time.localtime(time.time()).tm_sec
  if(sec % validation_sec == 0 and sec != used_sec):
	wii = validate_connection(wii)
	used_sec = sec

  buttons = wii.state['buttons']

  if (buttons & cwiid.BTN_PLUS):
    play_wav(thinking_prefix + thinking)

  if (buttons & cwiid.BTN_B):
    play_video('videos/dark-mark.mp4')

  if (buttons & cwiid.BTN_A):
    stop_video()

  if (buttons & cwiid.BTN_DOWN):
    play_wav(prefix + schools[1])

  if (buttons & cwiid.BTN_RIGHT):
    play_wav(prefix + schools[2])

  if (buttons & cwiid.BTN_LEFT):
    play_wav(prefix + schools[3])

  if (buttons & cwiid.BTN_UP):
    play_wav(prefix + schools[0])

  if (buttons & cwiid.BTN_MINUS):
    mixer.music.stop()
