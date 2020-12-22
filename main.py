#!/usr/bin/python
import board
import neopixel
import math
import time
import random

import os
stripsize = 150



pixels = neopixel.NeoPixel(board.D21, stripsize)
count =.1
max_pixels = 150
firing = []
occupied = []

chance = 10

# quick way to save a color
col_w = [255,255,45]
col_p = [255,0,255]
col_r = [255,0,0]
col_g = [0,255,0]
col_b = [0,0,255]
colours = [col_r, col_g, col_b, col_p, col_w]



# the following function maps a value from the target range onto the desination range
def translate(value, leftMin, leftMax, rightMin, rightMax):
	# Figure out how 'wide' each range is
	leftSpan = leftMax - leftMin
	if leftSpan == 0:
		leftSpan = 1
	rightSpan = rightMax - rightMin

	# Convert the left range into a 0-1 range (float)
	valueScaled = float(value - leftMin) / float(leftSpan)

	# Convert the 0-1 range into a value in the right range.
	return rightMin + (valueScaled * rightSpan)


# A single pixel
class Sparkle:

	def __init__(self,pos,rmax = 255,gmax = 255,bmax = 255,ticker = .01, interval = .01):
		#print("A Sparkle is born!")
		self.last_time = time.time()

		self.interval = interval
		self.pos = pos

		self.done = False

		self.ticks = -1.57079633
		self.ticker = ticker

		# I think these variables are for sine wave positioning?
		self.min = -1.57079633
		self.max = 4.71238898038 #1.57079633


		self.start = 0
		self.steps = 1024

		self.brightness = 255
		#self.rbrite = random.randint(0, rmax)
		self.rbrite = rmax
		#self.gbrite = random.randint(0, gmax)
		self.gbrite = gmax
		#self.bbrite = random.randint(0, bmax)
		self.bbrite = bmax

		#adds self to control lists
		occupied.append(pos)
		firing.append(self)

	# The following function draws this specific sparkle to the neopixel
	def draw(self):
		#Mark the time
		now = time.time()

		# Ensure the necessary time has passed since the last draw call (to keep everything consistent)
		if now - self.last_time > self.interval:
			#check to make sure the pixel isn't firing after its suppsoed to because idk why
			if not self.done:

				# for smoooooth fading I use only the best; SINE 
				# Ask your doctor is SINE is right for you!
				warp = math.sin(self.ticks)

				# following attempts to fade each element of the pixels colour evenly (needs work)
				valr = abs(int(translate(warp, -1, 1, 0, self.rbrite)))
				valg = abs(int(translate(warp, -1, 1, 0, self.gbrite)))
				valb = abs(int(translate(warp, -1, 1, 0, self.bbrite)))

				# once ready draws the pixel to screen
				pixels[self.pos] = (valr,valg,valb)

				# updates the ticker so we can calculate the right sine factor next draw.
				self.ticks += self.ticker

				# Kills the pixel once it's done a full ramp up and down.
				if self.ticks >= self.max:
					self.done = True
					pixels[self.pos] = (0,0,0)
					firing.remove(self)
					occupied.remove(self.pos)
					#print("A Sparkle has died!")

			self.last_time = now

# Controls all the pixels
class Shimmer:

	def __init__(self):
#		self.last_time = time.time()    # instance variable unique to each instance
#		self.interval = 1
		pass

	def show(self):
		#print(occupied)
		# Checks to makes sure there aren't too many sparkles firing
		if len(firing) < max_pixels:

			#picks a random number
			random.seed()
			randon = random.randint(0, chance)
			if randon < len(colours):
				this_colour = colours[randon]
			#use the random number to determine which sparkle we will make.
				this_sparkle = Sparkle(find_place(),rmax = this_colour[0],gmax = this_colour[1],bmax = this_colour[2], ticker = count, interval = 0)

			#if randon == 1:
				# nice warm light
#				this_sparkle = Sparkle(find_place(),rmax = 255,gmax = 255,bmax = 45, ticker = .01, interval = .0001)
# pink				this_sparkle = Sparkle(find_place(),rmax = 255,gmax = 0,bmax = 255, ticker = count, interval = 0)
				 #Choose a place for the new sparkle
			#	this_sparkle = Sparkle(find_place(),rmax = 0,gmax = 255,bmax = 0, ticker = count, interval = 0)
				# #Choose a place for the new sparkle
		#	if randon == 2:
		#		this_sparkle = Sparkle(find_place(),rmax = 255,gmax = 0,bmax = 0, ticker = count, interval = 0)

		#	if randon  == 3:
		#		this_sparkle = Sparkle(find_place(),rmax = 0, gmax = 0, bmax = 255, ticker = count, interval = 0)


		for sparkles in firing:
			sparkles.draw()


# recursive function to find an unoccupied place on the strip
def find_place():
	#randomly decide a pixel address
	place = random.randint(0, stripsize -1)

	#Check if that address is already in use.
	if place in occupied:
		#if it is start over
		return find_place()
	else:
		#if not return the adress found.
		return place

#pixels.clear()

scene = Shimmer()

while True:
#	print ("\033c")
	scene.show()
#	print(len(occupied))

				# # if we haven't reached full brightness yet
				# if self.r < 254:
					# # Brighten our sparkle (needs to be redone to include sine smoothing)
					# self.r += 1
					# self.g += 1
					# self.b += 1
				# else:
					# self.ascending = False
			# else:
					# self.r -= 1
					# self.g -= 1
					# self.b -= 1
					# if self.r < 1:
						# self.r = 0
						# self.g = 0
						# self.b = 0
						# self.done = True

#all fade 3 sine
	# val = abs(int((math.sin(tick/2) * 128) + 128))
	# val2 = abs(int((math.sin(tick + 3.1) * 128) + 128))
	# val3 = abs(int((math.sin(tick + 1.5) * 128) + 128))


	#trying to get shimmer working.
	# thistime = time.time()
	# if thistime - last_time >= interval:
		# randosparkle = random.randint(1, stripsize * 10) #picks a random number
		# last_time = thistime

	# for sparkles in firing:
			# sparkles.show()


	# for i in range(stripsize):
		# val = abs(int((math.sin(tick + (i*.06)) * 128) + 128))
		# val2 = 0#abs(int((math.sin(tick + (i*.08)+1) * 128) + 128))
		# val3 = abs(int((math.sin(tick + (i*.1)-1) * 128) + 128))
		# pixels[i] = (val,val2,val3)
		# #print("red: ", val, ", ", "Green: ", val2, ", ", "Blue ", val3)
		# #pixels.fill((val,val2,val3))
		# tick += .001	
#The following is the Cish version of the shimmer function
# /* SHIMMER FUNCTION */
# void shimmer()
# {

  # long presentTime = millis();
  # if((presentTime - previousTime) >= interval[0])
  # {
  # int randosparkle = random(0,(stripMax*10)); // picks a random number
  
  # for (int i=0; i <= (stripMax-1); i++)//For loop to check random number against magic numbers and set the pixel for activation
  # {
    # if (pixelData[i][5] == randosparkle && pixelData[i][0] == 0)
    # {
      # pixelData[i][0] = 1;
      # pixelData[i][1] = random(0,3);
    # }
  # }

        # for (int i=0; i <= (stripMax-1); i++)
        # {
            # if (pixelData[i][0] == 1)
            # {
                # drawPixel(i);
            # }
        # }
        # previousTime = presentTime;
  # }
# }
