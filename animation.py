from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time
import math

WIDTH = 128
HEIGHT = 64
TIME_VALUE = 3000 #in sec*0.5

button = Pin(8, Pin.IN, Pin.PULL_UP)#button
i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)#sda + scl
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
display.contrast(0x20)
#display.invert(1)

numberOfWalks = 0

class Clock:
    def __init__(self):
        self.timeleft = TIME_VALUE
        self.timefb = framebuf.FrameBuffer(bytearray(128 * 64), 128, 64, framebuf.MONO_HLSB)
        
    def tick(self):
        self.timeleft = self.timeleft - 1
        self.timefb.fill(0)
        percentage = round(128*self.timeleft/TIME_VALUE)
        self.timefb.fill_rect(0,0,percentage,5,1)
    
    def run(self):
        while self.timeleft > 0:
            for i in images:
                
                if self.timeleft == 0:
                    break
                clock.tick()
                renderScreen(i, True)
                time.sleep(0.5)
        global numberOfWalks
        numberOfWalks = numberOfWalks + 1
        return
    
def renderScreen(img, isTimerActive):
    fb.fill(0)
    if isTimerActive:
        fb.blit(clock.timefb, 0 , 2)
    fb.blit(img, 20, 10)
    fb.text(str(numberOfWalks), 20 , 30)
    display.blit(fb, 0, 0) 
    display.show()

def readImageFromFile(path):
    with open(path , 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
        fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    return fbuf
    
    
#load all images in /timmy
images = []
for n in range(4):
    fbuf = readImageFromFile('/timmy/timmy%s.pbm' % n)
    images.append(fbuf)
sleepingImage = readImageFromFile('/timmy/timmysleep.pbm')

while True:
    fb = framebuf.FrameBuffer(bytearray(128 * 64), 128, 64, framebuf.MONO_HLSB)
    if button.value() == 0:
        clock = Clock()
        clock.run()
    else:
        #print("Button is not Pressed")
        renderScreen(sleepingImage, False)
    time.sleep(0.25)
    

  