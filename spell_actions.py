from adafruit_servokit import ServoKit
import RPi.GPIO as gpio
import time

kit = ServoKit(channels=16)
trainOut = 80
trainIn = 10
boxOut = 180
boxIn = 90
skullOut = 0
skullIn = 90


gpio.setmode(gpio.BCM) # GPIO Numbers instead of board numbers
CANDLES = 26
COULDRON = 19
gpio.setup(CANDLES, gpio.OUT)
gpio.setup(COULDRON, gpio.OUT)
gpio.output(CANDLES, gpio.HIGH)
gpio.output(COULDRON, gpio.HIGH)
train = kit.servo[0]
box = kit.servo[1]
skull = kit.servo[3]

def start(test):
    global lock_status
    train.angle = trainIn
    box.angle = boxIn
    skull.angle = skullIn
    gpio.output(COULDRON, gpio.HIGH)
    gpio.output(CANDLES, gpio.HIGH)
    if(test):
        gpio.output(COULDRON, gpio.LOW)
        time.sleep(2)
        gpio.output(COULDRON, gpio.HIGH)
        gpio.output(CANDLES, gpio.LOW)
        time.sleep(2)
        gpio.output(CANDLES, gpio.HIGH)

def train_move():
    train.angle = trainIn
    time.sleep(.5)
    train.angle = trainOut
    time.sleep(2)
    train.angle = trainIn
    
def candle_on():
    gpio.output(CANDLES, gpio.LOW)
    
def candle_off():
    gpio.output(CANDLES, gpio.HIGH)
    
def couldron():
    gpio.output(COULDRON, gpio.LOW)
    time.sleep(15)
    gpio.output(COULDRON, gpio.HIGH)
    
def box_move():
    box.angle = boxOut
    time.sleep(5)
    box.angle = boxIn
    
def talk():
    #play(laugh)
    for x in range(0,50):
        skull.angle = skullOut
        time.sleep(0.1)
        skull.angle = skullIn
        time.sleep(0.1)

    
        
        
    
