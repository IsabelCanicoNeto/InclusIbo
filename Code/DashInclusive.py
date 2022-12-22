# import ButtonStuff.fliclib as fliclib

import asyncio
import struct
from bleak import BleakScanner
from bleak import BleakClient
import time
import simpleaudio as sa
import datetime
import logging
from os import listdir
import sys
from DashRobot import *
import random



#UUID = "001"
# p = True
# comportamento = False




class robot():
	def __init__(self, start_time = datetime.datetime.now(), condition="inclusive", speakerID1 = 1, speakerID2 = 2, speakerID3 = 3, name1 = "nome", name2 = "nome", name3 = "nome", state="empty", p = True, behaviorCond = "explicit"):

		# pace
		# self.condition = condition #
		self.startTime = start_time
		# self.behaviorCond = behaviorCond

		# robot ozo Dash
		self.dash = robotDash()

		# colours
		self.speakerID1 = speakerID1
		self.speakerID2 = speakerID2
		self.speakerID3 = speakerID3

		self.position = 0 # 0 : middle; speakerIDx
		self.angleposition = 0
		self.flagfirst = True
		# todo more than 3
		#self.speakerID4 = speakerID4
		#self.speakerID5 = speakerID5


		# adicionar NOMES todo ?

		# PARAM espaço
		self.headAngle = 50

		self.engageAngle = 2
		self.encourageAngle = 10
		self.driveDist = 200
		self.driveSpeed = 200
		self.driveDistEnc = 20
		self.driveSpeedEnc = 20
		self.driveDistTouch = 50
		self.slowPace = False
		self.turnAngle = 120


		#param Encourage Behaviour speech
		# Implicit
		# Encourage "mmm" "my3" (uhhh)
		self.EncourageI = []
		self.EncourageI.append ("huh")
		self.EncourageI.append ("my3")
		self.EncourageI.append ("yawn")
		self.EncourageI.append ("my4") # "mmm"

		# Follow implicit equals to encourage implicit
		self.FlwencI = self.EncourageI


		# Explicit
		# Encourage "mmm" "my3" (uhhh) + prefixo + name
		self.EncourageE = []
		self.EncourageE.append ("my2") # "é a tua vez"
		self.EncourageE.append ("my2name") # "é a tua vez"
		self.EncourageE.append ("") # "é a tua vez"

		# Follow implicit equals to encourage implicit prefixo + name
		self.FlwencE = []
		self.FlwencE.append ("okay") # sem nome e com nome
		self.FlwencE.append ("okayname") # okay com nome
		self.FlwencE.append ("confused8") # com nome
		self.FlwencE.append ("my4") # "mmm" nome

		self.lastminuteph = "my1"
		self.startsessionph = "my5"
		self.bye = "bye"

		self.p = p # print flag
		#self.warning = False

		if p:
			print("inicio")
			print(self.dash)




	#===============================================================================
	#
	#                              ROBOT EXPRESSIONS
	#
	#===============================================================================

	def executeExpression(self, expression, suggestedSpeaker, suggestedSpeakerName, actualSpeaker, actualSpeakerName, nextSpeaker, nextSpeakerName, movePace, organic = False, explicit=True):

		# adicionar a condição inclusive and control
		"""

		warning = False
		if lastround and not self.warning:  #only one warning
			warning = True
			self.warning = True
		"""


		if expression == "firstspeaker" : self.firstspeaker(suggestedSpeaker, suggestedSpeakerName, explicit)
		if expression == "turnexchange" :
			if suggestedSpeaker != nextSpeaker:
				explicit = True
				self.turnexchange(suggestedSpeaker, nextSpeaker, nextSpeakerName, movePace, organic,  explicit)
		if expression == "turnorgmed" :
			if suggestedSpeaker != nextSpeaker:
				explicit = True
				self.turnexchange(suggestedSpeaker, nextSpeaker, nextSpeakerName, movePace, organic, explicit)
		if expression == "teorganic":
			if suggestedSpeaker != nextSpeaker:
				self.turnexchange(suggestedSpeaker, nextSpeaker, nextSpeakerName, movePace, organic, False)
			else: self.flwencourage(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)

		if expression == "middle" : self.middle(suggestedSpeaker, 0, "", movePace, organic, False)
		if expression == "following" : self.following(suggestedSpeaker, actualSpeaker, actualSpeakerName, False)
		if expression == "encourage" : self.encourage(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)
		if expression == "flwencourage" : self.flwencourage(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)
		if expression == "end" : self.end(suggestedSpeaker, actualSpeaker, nextSpeaker, explicit)
		if expression == "engage" : self.engage(suggestedSpeaker, explicit)
		if expression == "lastminute" : self.lastminute(True)
		if expression == "startsession" : self.startsession(True)




	#===============================================================================
	#
	#                              ROBOT Behaviours
	#
	#===============================================================================

	'''
	************************************ First speaker  **************************************
	'''

	def firstspeaker(self, actualSpeaker, nameSpeaker, explicit):


		color = self.checkColor(actualSpeaker)

		self.firstspeaker_lights(True, color)
		#time.sleep(0.3)
		self.firstspeaker_mov("my2", actualSpeaker, nameSpeaker, explicit)
		#time.sleep(0.2)
		self.firstspeaker_lights(False, color)

	def firstspeaker_lights(self, firstTime, color):

		if firstTime :
			self.dash.stop()
			#time.sleep(0.2)
			self.dash.reset(4)
			#time.sleep(0.2)
			self.dash.all_color("black")
			#time.sleep(0.2)

		self.dash.eye_brightness(255)
		self.dash.tail_brightness(255)
		self.dash.eye(0b1010101010101)
		#time.sleep(0.0)
		self.dash.all_color(color)
		#time.sleep(0.0)
		self.dash.eye(8191)
		#time.sleep(0.0)




	def firstspeaker_mov(self, phrase, speaker, name, explicit):

		color = self.checkColor(speaker)
		driveDist, driveSpeed, angle, driveleaving = self.checkTurnmovement(self.speakerID1, speaker, False)

		if angle != 0 : self.dash.turn(angle)
		#time.sleep(0.5)

		self.dash.move(driveDist, driveSpeed)
		#time.sleep(0.5)
		self.position = speaker

		if explicit :
			self.dash.say(phrase)
			time.sleep(1.5)
			self.dash.say(name)
			self.dash.all_color(color)
			time.sleep(1)

		self.headpitch_mov(2)


	'''
	******************************** head pitch **************************************
	'''

	def headpitch_mov(self, number= 4):

		i = 0
		while i < number:
			self.dash.head_pitch(-2)
			# time.sleep(0.0)
			self.dash.head_pitch(2)
			#time.sleep(0.0)
			i += 1

		self.dash.head_pitch(0)


	def encouragemovcicle (self, number = 4)	:

		i = 0
		while i < number:
			self.dash.move(self.driveDistEnc, self.driveSpeedEnc)
			self.dash.move(-self.driveDistEnc, self.driveSpeedEnc)
			i += 1


	def headyaw_mov(self, angle, number= 2):

		i = 0
		angler = angle + self.angleposition
		anglel = self.angleposition - angle

		while i < number:

			self.dash.head_yaw(angler)
			# time.sleep(0.0)
			#self.dash.head_yaw(0)
			#time.sleep(0.0)
			angle = angle * (-1)
			self.dash.head_yaw(anglel)
			self.dash.head_yaw(self.angleposition)
			i += 1
		#self.dash.head_yaw(self.oldfwangle)



	'''
	******************************** turnexchange **************************************
	'''


	def turnexchange(self, suggestedSpeaker, nextSpeaker, nextSpeakerName, slowPace = False, organic = False,  explicit=True):

		#if warning :
		#	self.dash.say ("beep")
		#	time.sleep (0.5)

		colorNext = self.checkColor(nextSpeaker)
		self.turnexchange_lights(True, suggestedSpeaker, nextSpeaker, colorNext)

		self.turnexchange_mov(suggestedSpeaker, nextSpeaker, nextSpeakerName, "my2", colorNext, slowPace, organic, explicit)

		#self.turnexchange_lights(False, suggestedSpeaker, nextSpeaker, colorNext)

	def turnexchange_lights(self, firstTime, suggestedSpeaker, nextSpeaker, colorNext):


		if firstTime: self.dash.all_color("black")
		self.dash.eye(0b1010101010101)
		self.dash.eye(0b1101010101010)
		self.dash.all_color(colorNext)
		#if not firstTime: self.dash.eye(8191)



	def turnexchange_mov(self, suggestedSpeaker, nextSpeaker, name, phrase, color, slowPace, organic, explicit):
		if suggestedSpeaker == 0 : suggestedSpeaker = self.speakerID1 # todo 5Mar  suggestedSpeaker = self.speakerID1
		driveDist, driveSpeed, angle, driveleaving = self.checkTurnmovement(suggestedSpeaker, nextSpeaker, slowPace)
		self.dash.head_yaw(0)
		if self.position != 0 :
			self.dash.move(-driveDist, driveleaving) # only move robot to the middle if he is not there yet 10 Mar
		self.dash.turn(angle)
		self.dash.move(driveDist, driveSpeed)
		if explicit :
			self.dash.say(phrase)
			time.sleep(1.5)
			self.dash.say(name)
			self.dash.all_color(color)
			time.sleep(1)
		else:
			self.headpitch_mov(2)
		self.position = nextSpeaker

		""" touch 
		if organic : # TE in organic mode 
			self.dash.move(self.driveDistTouch , driveSpeed)
			self.headpitch_mov(4) # encourage
			self.dash.move(-self.driveDistTouch , driveSpeed)
		"""



	'''
	******************************** following **************************************
	'''

	def following(self, suggestedSpeaker, actualSpeaker, actualSpeakername, explicit=False):

		self.following_mov(suggestedSpeaker, actualSpeaker, actualSpeakername, explicit)


	def following_mov(self, suggestedSpeaker, actualSpeaker, actualSpeakername, explicit):
		# if the speaker is not the suggested one, move the head to him and head pitch, them return
		# if the speaker is the suggested one, move the head to him and head pitch, them return
		if self.position == 0  and suggestedSpeaker == 0 and self.flagfirst:
			self.flagfirst = False
			color = self.checkColor(actualSpeaker)
			self.dash.all_color(color)
			driveDist, driveSpeed, angle, driveleaving = self.checkTurnmovement(self.speakerID1, actualSpeaker, False)
			if angle != 0 : self.dash.turn(angle)
			self.dash.move(driveDist, driveSpeed)
			self.position = actualSpeaker

		elif suggestedSpeaker != 0:
			color = self.checkColor(suggestedSpeaker)
			self.dash.all_color (color)
			if suggestedSpeaker == actualSpeaker:
				self.dash.head_yaw(0)
				self.angleposition = 0
				self.engage(suggestedSpeaker)
				"""
				phrase = "my4"
				self.dash.say (phrase)
				"""
			else:
				angle = self.checkHeadmovement(suggestedSpeaker, actualSpeaker)
				if angle != self.angleposition :

					self.dash.head_yaw(angle)
					#time.sleep(0.2) # 1/2
				else: self.headpitch_mov(2)
					# if angle == 0 : self.headpitch_mov(2)
				#time.sleep(0.2) # 1/2




	'''
	******************************** encourage **************************************
	'''

	def encourage(self, suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit=True):
		self.encourage_mov(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)



	def encourage_mov(self, suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit):

		color = self.checkColor(suggestedSpeaker)
		if suggestedSpeaker == 0 :
			suggestedSpeakerName = self.startsessionph
			suggestedSpeaker = self.speakerID1


		self.dash.all_color (color)
		# return to the suggested speaker
		#angle = self.checkHeadmovement(suggestedSpeaker, actualSpeaker) todo rever
		self.angleposition = 0
		self.dash.head_yaw(self.angleposition)
		# self.dash.head_yaw(angle)
		self.encouragemovcicle(2)

		# Explicit behaviour
		if explicit :
			phrase = random.choice(self.EncourageE)

			if phrase == "my2name":
				phrase = "my2"
				self.dash.say (phrase)
				time.sleep(0.5) #1.5
			else:
				if phrase == "my2":
					self.dash.say (phrase)
					self.dash.all_color (color)
					time.sleep(1.5) #1.5
				self.dash.say (suggestedSpeakerName)
				time.sleep(0.5)



	'''
	******************************** Flwencourage **************************************
	'''

	def flwencourage (self, suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit=True):

		self.flwencourage_mov(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)



	def flwencourage_mov(self, suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit):


		color = self.checkColor(suggestedSpeaker)
		self.dash.head_yaw(0) # focus on suggested Speaker
		self.headpitch_mov(2)

		color = self.checkColor(suggestedSpeaker)
		self.dash.all_color (color)

		# Explicit behaviour
		if explicit :
			#1/2 sound for explicit
			# self.dash.say ("beep")
			#time.sleep (0.5)
			self.dash.eye(0b1010101010101)
			self.dash.eye(0b1101010101010)
			#1/2

			phrase = random.choice(self.FlwencE)

			if phrase == "okay" : # sem nome
				phrase = "okay"
				self.dash.say (phrase)
				time.sleep (1.5)
				self.dash.all_color (color)
			else: # com nome
				if phrase == "okayname":
					phrase = "okay"
				self.dash.say (phrase)
				time.sleep (1.5)
				self.dash.all_color (color)
		self.dash.head_pitch(0)
		#time.sleep(0.1)

	'''
	************************************ End  **************************************
	'''

	def end(self, sp1, sp2, sp3, explicit):

		self.end_lights(True, sp1, sp2, sp3)

		self.end_mov(sp1, sp2, sp3, explicit)

		self.end_lights(False, sp1, sp2, sp3)

	def end_lights(self, firstTime,  sp1, sp2, sp3):

		c1 = self.checkColor(sp1)
		c2 = self.checkColor(sp2)
		c3 = self.checkColor(sp3)

		if firstTime :
			self.dash.stop()

			self.dash.reset(4)

			self.dash.head_color(c1)
			self.dash.left_ear_color(c2)
			self.dash.right_ear_color(c3)


		else:
			self.dash.eye_brightness(255)
			self.dash.tail_brightness(255)
			self.dash.eye(0b1010101010101)

			self.dash.all_color("white")

			self.dash.all_color("black")

			self.dash.eye(8191)
			self.dash.say (self.bye)
			time.sleep (1.0)






	def end_mov(self, sp1, sp2, sp3, explicit):

		angle = 0
		self.angleposition = 0
		self.dash.head_yaw(0)
		angle = self.checkHeadmovement(sp1, sp2)
		self.dash.head_yaw(angle)

		angle = 0
		self.dash.head_yaw(angle)

		angle = self.checkHeadmovement(sp1, sp3)
		self.dash.head_yaw(angle)

		angle = 0
		self.dash.head_yaw(angle)


		self.dash.move(self.driveDist,self.driveSpeed)




	'''
	******************************** engage **************************************
	'''


	def engage(self, suggestedSpeaker, explicit=True):

		self.engage_lights(True, suggestedSpeaker)

		self.engage_movement (suggestedSpeaker)


	def engage_lights(self, firstTime, suggestedSpeaker):

		colorActual = self.checkColor(suggestedSpeaker)
		# colorNext = self.checkColor(nextSpeaker)
		self.dash.all_color ("black")
		self.dash.all_color(colorActual)
		self.dash.eye(0b1000000000000)
		self.dash.eye(0b1110000000000)
		self.dash.eye(0b1111100000000)
		self.dash.eye(0b1111111000000)
		self.dash.eye(0b1111111110000)
		self.dash.eye(0b1111111111100)
		self.dash.eye(8191)
		self.dash.all_color ("black")
		self.dash.all_color(colorActual)


	def engage_movement(self, suggestedSpeaker):

		angle = self.engageAngle

		self.headyaw_mov(angle, 1)


	'''
	******************************** middle **************************************
	'''


	def middle(self, suggestedSpeaker, nextSpeaker, nextSpeakerName, slowPace = False, organic = False, explicit=True):

		colorNext = self.checkColor(4)
		self.middle_lights(True, suggestedSpeaker, nextSpeaker, colorNext)

		self.middle_mov(suggestedSpeaker, nextSpeaker, nextSpeakerName, "my2", colorNext, slowPace, organic, explicit)

		self.middle_lights(False, suggestedSpeaker, nextSpeaker, colorNext)

	def middle_lights(self, firstTime, suggestedSpeaker, nextSpeaker, colorNext):


		if firstTime: self.dash.all_color("black")
		self.dash.eye(0b1010101010101)
		self.dash.eye(0b1101010101010)
		self.dash.all_color(colorNext)
		if not firstTime: self.dash.eye(8191)



	def middle_mov(self, suggestedSpeaker, nextSpeaker, name, phrase, color, slowPace, organic, explicit):

		driveDist, driveSpeed, angle, driveleaving = self.checkTurnmovement(suggestedSpeaker, nextSpeaker, slowPace)
		#self.dash.head_yaw(0)
		if self.position != 0 : self.dash.move(-driveDist, driveleaving) # only move robot to the middle if he is not there yet
		self.headpitch_mov(2)
		self.position = nextSpeaker

	'''
	******************************** startsession **************************************
	'''

	def startsession (self, explicit=True):

		#1/2 sound for explicit
		self.dash.stop()

		self.dash.say (self.startsessionph)
		time.sleep (1.5)

	'''
	******************************** Last minute **************************************
	'''

	def lastminute(self, explicit=True):

		#1/2 sound for explicit
		self.dash.say (self.lastminuteph)
		time.sleep (1.5)




#===============================================================================
	#
	#                              Other func
	#
	#===============================================================================


	def checkColor(self, speaker):

		if speaker == self.speakerID1: # red
			return "red"
		if speaker == self.speakerID2: # yellow
			return "yellow"
		if speaker == self.speakerID3: # blue
			return "blue"
		else:
			return "green"
		# todo more than 3




	def checkTurnmovement (self, actualSpeaker, nextSpeaker, slowPace):

		angle = self.turnAngle
		#actualSpeaker = self.position
		if self.position != 0 :
			actualSpeaker = self.position

		driveDist = self.driveDist
		driveSpeed = self.driveSpeed
		driveSpeedtalking = driveSpeed # if talking

		if slowPace :  # slower pace, inclusive configuration
			driveSpeedtalking = driveSpeed/4 # 2 10 Mar

		if (actualSpeaker == nextSpeaker):
			return driveDist, driveSpeed,0,  driveSpeedtalking

		if (actualSpeaker == self.speakerID1):
			if (nextSpeaker == self.speakerID3):

				return driveDist, driveSpeed,angle,  driveSpeedtalking
			else:
				angle = -1*angle
				return driveDist, driveSpeed,angle,  driveSpeedtalking

		if (actualSpeaker == self.speakerID2) :
			if (nextSpeaker == self.speakerID1):
				return driveDist, driveSpeed,angle,  driveSpeedtalking
			else:
				angle = -1*angle
				return driveDist, driveSpeed,angle,  driveSpeedtalking

		if (actualSpeaker == self.speakerID3) :
			if (nextSpeaker == self.speakerID2):
				return driveDist, driveSpeed,angle,  driveSpeedtalking
			else:
				angle = -1*angle
				return driveDist, driveSpeed,angle, driveSpeedtalking

	def checkHeadmovement (self, suggestedSpeaker, actualSpeaker):

		angle = self.headAngle
		if suggestedSpeaker == 0 : suggestedSpeaker = self.speakerID1

		if (suggestedSpeaker == actualSpeaker):
			angle = 0
			return angle

		if (suggestedSpeaker == self.speakerID1):
			if (actualSpeaker == self.speakerID2):
				return angle
			else:
				angle = -1*angle
				return angle

		if (suggestedSpeaker == self.speakerID2) :
			if (actualSpeaker == self.speakerID3):
				return angle
			else:
				angle = -1*angle
				return angle

		if (suggestedSpeaker == self.speakerID3) :
			if (actualSpeaker == self.speakerID1):
				return angle
			else:
				angle = -1*angle
				return angle