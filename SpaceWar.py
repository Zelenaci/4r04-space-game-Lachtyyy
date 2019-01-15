# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 11:17:12 2019
@author: lachtyyy
"""

import pyglet
import random
from math import sin, cos, radians, pi
from pyglet.window.key import DOWN, UP, LEFT, RIGHT

window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()   # pro optimalizované vyreslování objektů

class SpaceObject(object):

    def __init__(self,x=None, y=None,direction=None,speed=None, rspeed=None):
        
        self.image = pyglet.image.load('meteorBrown_big1.png')
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        self.sprite = pyglet.sprite.Sprite(self.image, batch=batch)
        self._x = x if x is not None else random.randint(600, window.width)
        self._y = y if y is not None else random.randint(600, window.height)
        self.x = self._x
        self.y = self._y
        self.direction = direction if direction is not None else random.randint(0, 359)
        self.speed = speed if speed is not None else random.randint(50, 200)
        self.rspeed = rspeed if rspeed is not None else random.randint(-40, 40)

    def tick(self, dt):
        self.bounce()
        
        self.x += dt * self.speed * cos(pi / 2 - radians(self.direction))
        self.sprite.x = self.x
        self.y += dt * self.speed * sin(pi / 2 - radians(self.direction))
        self.sprite.y = self.y
        self.sprite.rotation += 0.01 * self.rspeed
        
    def bounce(self):
        rozmer = min(self.image.width, self.image.height)/2
        if self.x + rozmer >= window.width:
            self.direction = random.randint(190, 350)
            return
        if self.x - rozmer <= 0:
            self.direction = random.randint(10, 170)
            return
        if self.y + rozmer >= window.height:
            self.direction = random.randint(100, 260)
            return
        if self.y - rozmer <= 0:
            self.direction = random.randint(-80, 80)
            return
    
        
class Raketa(object):

    def __init__(self):
        #načtu obrázek lodě
        self.obrazek = pyglet.image.load("playerShip1_blue.png")
        #střed otáčení dáme do prostřed tohoto obrázku
        self.obrazek.anchor_x = self.obrazek.width // 2
        self.obrazek.anchor_y = self.obrazek.height // 2
        #z obr. vytovoříme sprite
        self.sprite =pyglet.sprite.Sprite(self.obrazek, batch=batch)
        self.sprite.rotation = 50
        self.speed = 350
        self.x = 400
        self.y = 200
        self.sprite.x = self.x
        self.sprite.y = self.y
        
    def tick(self, dt):
        global keyboard
        self.okraj()
        for data in keyboards:
            if data == LEFT:
                self.sprite.rotation -= 5
            if data == RIGHT:
                self.sprite.rotation += 5
            if data ==  UP:
                self.x = self.x + self.speed*dt*sin(pi*self.sprite.rotation/180)
                self.sprite.x = self.x
                self.y = self.y + self.speed*dt*cos(pi*self.sprite.rotation/180)
                self.sprite.y = self.y
            if data == DOWN:
                self.x = self.x + self.speed*dt-sin(pi*self.sprite.rotation/180)
                self.sprite.x = self.x
                self.y = self.y + self.speed*dt-cos(pi*self.sprite.rotation/180)
                self.sprite.y = self.y
         
    def okraj(self):
        rozmer = min(self.obrazek.width,self.obrazek.height)/2
        if self.x + rozmer >= window.width+60:
            self.sprite.x=-20
        if self.x - rozmer < -60:
            self.sprite.x=window.width+20
        if self.y + rozmer >= window.height + 60:
            self.sprite.y=-20
        if self.y - rozmer < -60:
            self.sprite.y=window.height+20

keyboards=set()        
for o in range(1):
    lod=Raketa()
    pyglet.clock.schedule_interval(lod.tick, 1/ 60 )

for x in range(15):
    kamen=SpaceObject()
    pyglet.clock.schedule_interval(kamen.tick, 1/ 60 )





@window.event
def on_key_press(data, mod):
    global keyboards
    keyboards.add(data)
    
@window.event
def on_key_release(data, mod):
    global keyboards
    keyboards.remove(data)

@window.event
def on_draw():
    window.clear()
    batch.draw()
 
    
    
pyglet.app.run() 
