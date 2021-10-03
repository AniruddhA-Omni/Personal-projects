import pyglet
import time
sound = pyglet.media.load("sound.wav",streaming=False)
l_sound = pyglet.media.load("left.wav", streaming=False)
r_sound = pyglet.media.load("right.wav", streaming=False)
sound.play()
time.sleep(1)
l_sound.play()
time.sleep(1)
r_sound.play()
time.sleep(1)
