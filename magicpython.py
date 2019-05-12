import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import spell_actions

test = False
oldpt = (0,0)
dx = 0
dy = 0
oldCh = ''
SpellWait = True
waitclear = False
sensitivity1 = 20
sensitivity2 = -20
numclear = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)
spell_actions.start(test)

def spellMatch(str):
    if str == "lu" and SpellWait:
        print("Lumos! You cast a spell!")
        spell_actions.candle_on()
        clear()
    if str == "ul" and SpellWait:
        print("Alohomora!")
        spell_actions.box_move()
        clear()
    if str == "ru" and SpellWait:
        print("Nox!")
        spell_actions.candle_off()
        clear()
    if str == "ur" and SpellWait:
        print("Incendio!")
        spell_actions.couldron()
        clear()
    if str == "ld" and SpellWait:
        print("Accio!")
        spell_actions.train_move()
        clear()
    if str == "ud" and SpellWait:
        print("animate")
        spell_actions.talk()
        clear()

def addSpell(dir):
    global oldCh
    spellMatch(oldCh + dir)
    oldCh = dir


def FindSpell(x,y):
    global waitclear
    #print ("Finding Spell...\n")
    #print ("dx: " + str(x) + "  dy: " + str(y) + "\n")
    if y < sensitivity2:
        print("Up")
        addSpell("u")
            
    if y > sensitivity1:
        print("D0wn")
        addSpell("d")
            
    if x < sensitivity2:
        print("Left")
        addSpell("l")
            
    if x > sensitivity1:
        print("Right")
        addSpell("r")

def waitClear(dx, dy):
    global oldCh, SpellWait, waitclear, oldpt, numclear
    if abs(dx)< sensitivity1 and abs(dy) < sensitivity1 :
        print("clearing due to wait")
        if numclear > 10:
            SpellWait = True
            
        waitclear = False
        oldCh = ''
        oldpt = (0,0)
        numclear = numclear + 1
        
def clear():
    global oldCh, SpellWait, oldpt, numclear
    SpellWait = False
    oldCh = ''
    oldpt = (0,0)
    numclear = 0


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    global oldpt, SpellWait
    image = frame.array
 
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    #print(maxLoc)
    dx = maxLoc[0] - oldpt[0]
    dy = maxLoc[1] - oldpt[1]
    if bool(oldpt == (0,0)) != bool(maxLoc == (0,0)):
        SpellWait = False
        dx = 0
        dy = 0
        
    FindSpell(dx, dy)
    waitClear(dx, dy)
    oldpt = maxLoc
    cv2.imshow('Harry Potter', image)
    key = cv2.waitKey(1) & 0xFF
    time.sleep(0.1)
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
	    break

