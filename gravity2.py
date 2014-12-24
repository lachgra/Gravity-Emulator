#!/usr/bin/env python

# Copyright (C) 2014 Lachie Grant <https://github.com/lachgra>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import pygame
from pygame.locals import *
from time import sleep
from sys import exit
from random import randint
from decimal import Decimal
import math
import sys
import subprocess
import threading

# start pygame
pygame.init()
pygame.time.Clock()

if len(sys.argv) > 2 and sys.argv[1] == "-s":
	screen_size = sys.argv[2].split('x')
	for i in range(2):
		screen_size[i] = int(screen_size[i])
	width, height = screen_size
	
else:
	width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
	screen_size = (width, height)

# screen parameters
pygame.display.set_mode(screen_size)
screen = pygame.display.set_mode(screen_size, 0, 32)
fullscreen = False

# set the background
background = pygame.Surface(screen.get_size()).convert()
background.fill((250, 250, 250))

# caption the window
pygame.display.set_caption("Physics Emulator")

# main loop parameters
rainbow = True
gravity = True
coords = False
removed = False

# text definitions
calibri16 = pygame.font.SysFont("calibri", 16)
calibri32 = pygame.font.SysFont("calibri", 32)

# class and function definitions
class particle:
	def __init__(self, size, central=False):
		self.initialize(central)
		self.size = size # size of the object
		self.colours = [randint(0,255), randint(0,255), randint(0,255)]
	
	def update(self):
		if rainbow:
			r,g,b = randint(0,255), randint(0,255), randint(0,255)
			self.circle = pygame.draw.circle(screen, (r,g,b), (self.x, self.y), self.size)

		if self.x >= width - 50: 	   # right side
			self.vx = -3
		if self.x <= 50:   	   	   # left side
			self.vx = 3
		if self.y <= 0:	 	   # ceiling
			self.vy = -(self.vy)/2
		if self.y == height:
			self.vy = -(self.vy)/2
		if self.y > height - self.size - 1:
			self.vy = -(self.vy)
			self.y = height - self.size - 1

		pygame.draw.circle(screen, self.colours, (self.x, self.y), (self.size))
		
		self.vy += self.ay     # change in velocity
		self.vx += self.ax 
		
		self.x += self.vx      # change in position
		self.y += self.vy

		if gravity:
			for mass in objects:
				distance = math.sqrt((self.y_dist(mass)**2) + (self.x_dist(mass)**2))
				if self.x > mass.x:   # right of
					self.vx -= int(round(self.x_dist(mass)*mass.size)/(15000))
				elif self.x < mass.x: # left of
					self.vx += int(round(self.x_dist(mass)*mass.size)/(15000))
				else:
					pass
			
				if self.y > mass.y:   # below
					self.vy -= int(round(self.y_dist(mass)*mass.size)/(15000))
				elif self.y < mass.y: # above
					self.vy += int(round(self.y_dist(mass)*mass.size)/(15000))
				else:		      # on
					pass

				if distance > 0 and distance < mass.size:
					#self.dy = -(self.dy/3)
					#self.dx = -(self.dx/3)
					pass

	def x_dist(self, obj):
		return abs(self.x - obj.x)
		
	def y_dist(self, obj):
		return abs(self.y - obj.y)
				
	def initialize(self, central):
		if central:
			self.x, self.y, self.vx, self.vy, self.ax, self.ay = 800, 500, 0, 0, 0, 0
		else:
			vx, vy, ax, ay = 0, 0, 0, 0
			self.x, self.y, self.vx, self.vy, self.ax, self.ay = randint(0, width), randint(0, height), vx, vy, ax, ay
			
	def blend_colour(self, colour1, colour2, blend_factor):
		r1, g1, b1 = colour1
		r2, g2, b2 = colour2
		red = r1+(r2-r1)*blend_factor
		green = g1+(g2-g1)*blend_factor
		blue = b1+(b2-b1)*blend_factor
		return [int(red), int(green), int(blue)]
		
def create_particle(n=1, size=randint(20,50)):
	objects = []
	for i in range(n):
		objects.append(particle(size, False))
	return objects
	
	
def persistents(mx, my):
	# mouse position
	text = str(mx) + ", " + str(my)
	screen.blit(calibri32.render(text, True, (0, 0, 0)), (5, 5))

	x1, y1, xl, yl = 5, 30, 100, 30
	if removed:
		text = "Add Mass"
	else:
		text = "Remove mass"	
	pygame.draw.rect(screen, (0, 0, 0), (x1, y1, xl, yl))
	screen.blit(calibri16.render(text, True, (255, 255, 255)), (x1+3, y1+8))

	x1, y1, xl, yl = 5, 70, 100, 30	
	if gravity:
		text = "Gravity is ON"
	else:
		text = "Gravity is OFF"
	pygame.draw.rect(screen, (0, 0, 0), (x1, y1, xl, yl))
	screen.blit(calibri16.render(text, True, (255, 255, 255)), (x1+3, y1+8))
	
	x1, y1, xl, yl = 5, 110, 100, 30	
	text = "Add Particle"
	pygame.draw.rect(screen, (0, 0, 0), (x1, y1, xl, yl))
	screen.blit(calibri16.render(text, True, (255, 255, 255)), (x1+3, y1+8))
	
	
	x1, y1, xl, yl = 5, 150, 100, 30
	if fullscreen:
		text = "Windowed"
	else:
		text = "Fullscreen"
	pygame.draw.rect(screen, (0, 0, 0), (x1, y1, xl, yl))
	screen.blit(calibri16.render(text, True, (255, 255, 255)), (x1+3, y1+8))
	
	x1, y1, xl, yl = 5, 190, 100, 30
	text = "Quit"
	pygame.draw.rect(screen, (0, 0, 0), (x1, y1, xl, yl))
	screen.blit(calibri16.render(text, True, (255, 255, 255)), (x1+3, y1+8))

if __name__ == "__main__":
	p = particle(20)
	m = particle(300, True)
	objects = [m,p]
	# main loop
	while True:
		mx, my = pygame.mouse.get_pos()
		persistents(mx, my)
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:	
				if mx >= 5 and mx <= 75 and my >= 30 and my <= 70: # remove the mass TODO
					pass

				if mx >= 5 and mx <= 75 and my >= 70 and my <= 100: # gravity button
					gravity = not gravity
					if gravity:
						for i in objects:
							i.initialize(False)
					print "Gravity is now " + str(gravity)
					
				if mx >= 5 and mx <= 75 and my >= 110 and my <= 140: # more particles
					to_add = create_particle(1)
					for i in to_add:
						objects.append(i)
					print "Added a particle"
					
					
				if mx >= 5 and mx <= 75 and my >= 150 and my <= 180:
					fullscreen = not fullscreen
					if fullscreen:
						screen = pygame.display.set_mode(screen_size, FULLSCREEN, 32)
					else:
						screen = pygame.display.set_mode(screen_size, 32)
					print "Fullscreen is now " + repr(fullscreen)
				
				if mx >= 5 and mx <= 75 and my >= 190 and my <= 220:
					print "Exiting"
					exit()

			if event.type == KEYDOWN:
				if event.key == K_UP:
					for i in objects:
						i.ay -= 2                # Y UP FORCE
					print "The y up force has been applied"
					
				if event.key == K_DOWN:
					for i in objects:
						i.ay += 2                # Y DOWN FORCE
					print "The y down force has been applied"
			
				if event.key == K_LEFT:
					for i in objects:
						i.ax -= 2 	 	 # X LEFT FORCE
					print "The x left force has been applied"
			
				if event.key == K_RIGHT:	
					for i in objects:
						i.ax += 2        	 # X RIGHT FORCE
					print "The x right force has been applied"
				
				if event.key == K_SPACE:
					for i in objects:
						i.initialize(False)
						gravity = False
					print "Reset all objects"
					print "Gravity is now " + str(gravity)
			
				if event.key == K_LSHIFT or event.key == K_RSHIFT:
					for i in objects:
						i.vx = randint(-5,5)
						i.vy = randint(-5,5)
				
				if event.key == K_f:
					fullscreen = not fullscreen
					if fullscreen:
						screen = pygame.display.set_mode(screen_size, FULLSCREEN, 32)
					else:
						screen = pygame.display.set_mode(screen_size, 32)
			
				if event.key == K_c:
					background.fill((randint(0,255), randint(0,255), randint(0,255))) # Random background
				
				if event.key == K_q:
					exit()
				
				if event.key == K_r:
					rainbow = not rainbow
				if event.key == K_b:
					to_add = create_particle(10)
					for i in to_add:
						objects.append(i)
					print len(objects)
				
				if event.key == K_t:
					time_var = time_var * 0.5

			if event.type == KEYUP:
				if event.key == K_UP:
					for i in objects:
						i.ay += 2 # No force applied
					print "The y up force has been removed"
			
				if event.key == K_DOWN:
					for i in objects:
						i.ay -= 2 # No force applied
					print "The y down force has been removed"
				
				if event.key == K_LEFT:
					for i in objects:
						i.ax += 2 
					print "The x left force has been removed"
			
				if event.key == K_RIGHT:
					for i in objects:
						i.ax -= 2
					print "The x right force has been removed"

			if event.type == QUIT:
				print "Exiting"
				exit()

		screen.blit(background, (0,0)) # resets the background
		persistents(mx, my)
		for i in objects:
			i.update()

		pygame.display.update()
	
		
