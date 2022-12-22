# import ButtonStuff.fliclib as fliclib

import asyncio
import struct
from bleak import BleakScanner
from bleak import BleakClient
import time
import simpleaudio as sa
import datetime
import logging
import pathlib
from os import listdir
import sys
import random
from DashInclusive import *



#UUID = "001"
# p = True
# comportamento = False





class activityRobot():
	def __init__(self, start_time = datetime.datetime.now(), condition="encouragedriven", speakerID1 = 1, speakerID2 = 2, speakerID3 = 3, name1 = "nome", name2 = "nome", name3 = "nome", cID1 = "nome", cID2 = "nome", cID3 = "nome", grpID = 0, state="empty", p = True):


		# condition
		self.condition = condition
		self.startTime = start_time
		self.counttime = False # count time recorded as speaker todo update 5Mar consider that talk lower than minspeech is noise

		#self.behavior_cond = behavior_cond # remove
		if self.condition == "encouragedriven" or self.condition == "control":
			self.organicspeech = False # flag true if organic speech ; false if not
		else:
			self.organicspeech = True

		# robot

		if self.condition == "baseline":
			self.robot = -1
		else:
			self.robot = robot(start_time, condition, speakerID1, speakerID2, speakerID3, p)

		self.robot_log = []

		# speakers information

		self.speakerID1 = speakerID1
		self.speakerID2 = speakerID2
		self.speakerID3 = speakerID3
		self.organicID = 0
		self.childID1 = cID1
		self.childID2 = cID2
		self.childID3 = cID3
		self.name1 = name1
		self.name2 = name2
		self.name3 = name3
		self.grpID = grpID


		# conversation information
		listspeakers = [speakerID1,speakerID2,speakerID3]
		firstspeaker = random.choice(listspeakers)
		self.firstround = True

		if self.organicspeech :
			self.actualSpeaker = 0 # speakerID1
			self.newSpeaker = 0
			self.suggestedSpeaker = 0 # self.actualSpeaker
			self.startSuggestedUser = -1
			self.startOrgSpeech = -1
			self.endOrgSpeech = -1
			self.teorganic = 1
		else:
			print ("RUN: First speaker " + str(firstspeaker))
			self.actualSpeaker = firstspeaker
			self.newSpeaker = 0
			self.suggestedSpeaker = self.actualSpeaker
			self.startSuggestedUser = self.startTime
			self.startOrgSpeech = -1
			self.endOrgSpeech = -1
			print ("RUN: First speaker " + str(self.suggestedSpeaker))


		self.speakingTimeID1 = 0.0
		self.speakingTimeID2 = 0.0
		self.speakingTimeID3 = 0.0

		self.speakingInterruptTimeID1M = 0.0 # time ID1 interrupt in mediated speech
		self.speakingInterruptTimeID2M = 0.0 # time ID2 interrupt  in mediated speech
		self.speakingInterruptTimeID3M = 0.0 # time ID3 interrupt  in mediated speech

		self.speakingInterruptedbyTimeID1M = 0.0 # time ID1  was interrupted by others  in mediated speech
		self.speakingInterruptedbyTimeID2M = 0.0 # time ID2 was interrupted by others  in mediated speech
		self.speakingInterruptedbyTimeID3M = 0.0 # time ID3 was interrupted by others  in mediated speech

		self.speakingInterruptTimeID1O = 0.0 # time ID1 interrupt when in organic speech
		self.speakingInterruptTimeID2O = 0.0 # time ID2 interrupt in organic speech
		self.speakingInterruptTimeID3O = 0.0 # time ID3 interrupt in organic speech

		self.speakingInterruptedbyTimeID1O = 0.0 # time ID1  was interrupted by others in organic speech
		self.speakingInterruptedbyTimeID2O = 0.0 # time ID2 was interrupted by others in organic speech
		self.speakingInterruptedbyTimeID3O = 0.0 # time ID3 was interrupted by others in organic speech

		self.speakingSSoutTimeID1 = 0.0 # time ID1 is talking without being SS
		self.speakingSSoutTimeID2 = 0.0 # time ID2 is talking without being SS
		self.speakingSSoutTimeID3 = 0.0 # time ID3 is talking without being SS

		self.speakingSSinTimeID1 = 0.0 # time ID1 is talking being SS
		self.speakingSSinTimeID2 = 0.0 # time ID2 is talking being SS
		self.speakingSSinTimeID3 = 0.0 # time ID3 is talking being SS

		self.speakingOrgTimeID1 = 0.0 # time ID1 is talking in organic conversation
		self.speakingOrgTimeID2 = 0.0 # time ID2 is talking in organic conversation
		self.speakingOrgTimeID3 = 0.0 # time ID3 is talking in organic conversation


		self.speakingMedTimeID1 = 0.0 # time ID3 is talking in no organic conversation (assumed minimum minspeech)
		self.speakingMedTimeID2 = 0.0 # time ID3 is talking in no organic conversation (assumed minimum minspeech)
		self.speakingMedTimeID3 = 0.0 # time ID3 is talking in no organic conversation (assumed minimum minspeech)

		# inclusion metrics
		self.belonginessRID1 = 0.0
		self.belonginessRID2 = 0.0
		self.belonginessRID3 = 0.0

		self.encourageRID1 = 0.0
		self.encourageRID2 = 0.0
		self.encourageRID3 = 0.0

		self.TERID1 = 0.0
		self.TERID2 = 0.0
		self.TERID3 = 0.0

		self.flwencourageRID1 = 0.0
		self.flwencourageRID2 = 0.0
		self.flwencourageRID3 = 0.0

		self.followingRID1 = 0.0
		self.followingRID2 = 0.0
		self.followingRID3 = 0.0

		self.TEorgRID1 = 0.0
		self.TEorgRID2 = 0.0
		self.TEorgRID3 = 0.0

		self.middleRID1 = 0.0
		self.middleRID2 = 0.0
		self.middleRID3 = 0.0

		self.engageRID1 = 0.0
		self.engageRID2 = 0.0
		self.engageRID3 = 0.0

		# state
		self.state = state
		self.previousState="empty"
		self.startState = time.time()


		# logging values
		self.activatedExpression = {}
		self.logExpression = []
		self.logStates = []
		self.logSpeaker = []
		self.logTimePerExpression = []
		self.count = 0
		self.p = p # print flag
		self.logSpeaker.append((self.grpID, self.suggestedSpeaker, self.startTime))

		print("inicio")
		print(self.robot)


		# configuration values

		self.minspeech = 0.5 # 1.0 # number of seconds to record speaking times # todo update 5Mar
		self.minspeech2move = 1.0 # number of seconds to evaluate a move in talking state ( organic speaker change or following, praising , TE or mixed-up)
		# self.minspeech2chspeaker = 5.0 # number of seconds to evaluate a change of speaker
		self.minfollowing = 0.5 # 1.0 # number of speaking seconds to evaluate following expression 5.0 todo (micbot 150 ms, decide if 2s is ok or move to 1s
		self.minengage = 2.0 # number of speaking seconds to evaluate engage expression 5.0
		self.minencourage = 4.0  # 5 Mar 4.0 # number of speaking seconds to evaluate encourage expression todo so se aplica em qd nao esta a falar
		self.minflwencourage = 4.0 # 5Mar 4.0 # number of speaking seconds to evaluate flwencourage

		# mediate control and encouragedriven
		self.minTE = 15.0 # number of speaking seconds to evaluate TE

		# organic follow
		self.minTEorgmed = 60.0  #   number of speaking seconds to evaluate moving from organic to mediated turn exchange
		self.minTEorgnotmed = 20.0 #   number of speaking seconds to evaluate moving from mediated to organic turn exchange
		self.minTEorganic = 3.0 # 5Mar 4.0 # number of speaking seconds to evaluate an organic turn exchange, and move closer to the new speaker


		# overlap not used
		self.minoverlap = 2 * self.minspeech2move # number of seconds to evaluate overlap in talking state
		self.minWoverlap = self.minspeech2move # number of seconds to evaluate overlap in talking state

		# 5 x idle expresion values
		self.minidle = 2.0 # number of seconds to evaluate new expression after idle
		self.minidlefollowing = 100.0 # number of seconds to evaluate following in idle state
		self.minidleflwencourage = 100.0 # number of seconds to evaluate flwencourage in idle state
		self.minidleencourage = 2.0 # number of seconds to evaluate encourage  in idle state
		self.minidleTE = 10.0 # number of seconds to evaluate TE in idle state
		self.minidleengage = 2.0 # repeat start session with
		self.minidleTEorg = 15.0 # number of seconds to evaluate to move to the middle  and change to organic in idle state
		#self.minTEorganicidle = 2.0 # number of speaking seconds to evaluate an organic turn exchange, and move closer to the new speaker

		# configuration behaviour values
		self.maxexpEncTimes = 1 # number of times to repeat encouragement in explicit behav (2)

		self.maxexpFlwTimes = 1 # number of times to repeat flwencourage in explicit behav
		self.maximpEncTimes = 1 # number of times to repeat encouragement in implicit behav

		self.maximpFlwTimes = 1 # number of times to repeat flwencourage in implicit behav
		self.maxexpFollowTimes = 10 # number of times to repeat following (4)
		self.explicit = False
		self.slowpace = False
		self.lastround = False

		self.following = 0
		self.encourage = 0
		self.flwencourage = 0
		self.teorganic = 0
		self.te = 0
		self.engage = 0
		self.middle = 0


		self.numlround = 0






# loop.run_until_complete(self.connectRobot())
		# loop.stop()


	def finishActivity(self): # validar com erros

		logTotalTimePerExpression = {}

		if self.condition != "baseline" : self.robot.dash.closeDash()
		"""
		for (e,d) in self.logTimePerExpression:
			if e not in logTotalTimePerExpression.keys():
				logTotalTimePerExpression[e] = d
			else:
				logTotalTimePerExpression[e] = logTotalTimePerExpression[e] + d
		"""

		log_directory = f"logs/{self.condition}/{self.grpID}/"
		pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)


		file = f"{log_directory}/robot_logs_{self.grpID}_{self.startTime}.log"
		
		logging.basicConfig(filename=file, level=logging.DEBUG)
		logging.info("======CONDITION======")
		logging.info(self.condition)
		logging.info("======Expressions ======")
		logging.info(self.logExpression)
		logging.info("======STATE CHANGES======")
		logging.info(self.logStates)
		logging.info("======Suggested/atual speaker  CHANGES======")
		logging.info(self.logSpeaker)
		# VALIDAR TEMPOS POR SPEAKER, STATE ....
		logging.info("======Expressions TIMES======")
		logging.info(self.logTimePerExpression)
		#logging.info("======ROOM TOTAL TIMES======")
		#logging.info(logTotalTimePerRoom)

		self.robot_log = []
		self.robot_log.append(self.condition)
		self.robot_log.append(self.logSpeaker)
		self.robot_log.append(self.logStates)
		self.robot_log.append(self.logExpression)
		#self.robot_log.append(self.logTimePerExpression)

		print ("robot_log", self.robot_log)




	def checkFileName(self):
		files = listdir('Logs')

		if len(files) == 0:
			return "1"
		else:
			splitedFiles = []
			for f in files:
				name = f.split('.')[0]
				splitedFiles.append(name)
			splitedFiles.sort()
			numberPart = splitedFiles[-1]
			#numberPart = files[-1].split('.')[0]
			number = int(numberPart) + 1
			return str(number)

#===============================================================================
#
#                              Situation analysis
#
#===============================================================================


	def checknextactivity(self, statusSpeech, startState, overlap, Speaker, other_mic1ID, other_mic2ID, mic_speakingTime, othermicID1_speakingTime, othermicID2_speakingTime, speechduration):

		atualtime = time.time()
		durationstate = atualtime - startState
		durationsession = atualtime - self.startTime


		self.updateSpeakingTime (Speaker, other_mic1ID, other_mic2ID, mic_speakingTime, othermicID1_speakingTime, othermicID2_speakingTime)


		if statusSpeech == "idle":

			triggerExp = round (speechduration % self.minidle, 1)
			# if self.p : print ("start checking idle expression")
			#print (f"duration {speechduration} min speech {self.minspeech} and ratio {speechduration % self.minspeech} and trigger {triggerExp}")
			if (triggerExp == 0.0) and (speechduration >= self.minidle) and (self.organicspeech or (Speaker == self.suggestedSpeaker)) :

				# x seconds minimium for checking new expression   eg 5.0 and check the suggested Speaker trigger (to avoid having three)

				if self.p: print (f" ACT: start checking idle expression para mover {datetime.datetime.now()}")

				#atualtime = time.time()
				if (self.state != statusSpeech) or (self.startState != startState):
					self.state = statusSpeech
					self.startState = startState

					self.logStates.append (( statusSpeech , startState, durationstate, self.grpID, Speaker, self.suggestedSpeaker, self.organicspeech, self.startOrgSpeech, self.endOrgSpeech, self.startSuggestedUser, speechduration))


				print (f"statusSpeech {statusSpeech} duration state {durationstate} speaker {Speaker} duration speech {speechduration} min speech {self.minspeech}  time {datetime.datetime.now()} session duration {durationsession}")
				# todo include idle reactions

				goAheadEngage, goAheadTEmed, goAheadTEorganic, goAheadFollowing, goAheadEncourage,  goAheadFlwencourage, goAheadTE = self.validateNextExpr (statusSpeech, Speaker, other_mic1ID, other_mic2ID, speechduration, atualtime)
				print ( f"ACT flags En : {goAheadEngage} TEM { goAheadTEmed} TEO {goAheadTEorganic}  TE {goAheadTE} Fw {goAheadFollowing} Enc {goAheadEncourage} Flen {goAheadFlwencourage}" )

				if goAheadTE :
					self.validateNewSpeaker (self.counttime)
					if (self.newSpeaker != self.suggestedSpeaker):
						self.slowpace = (self.actualSpeaker == self.suggestedSpeaker) # 10MAr
						goAhead = self.func ("turnexchange")
						if goAhead :
							#self.te = 1 #mark beginning TE
							self.updateSpeakerTE ()
							self.updateBelonginessRate(self.suggestedSpeaker, "turnexchange")
							self.updateExplicit("turnexchange")


				elif goAheadEncourage :
					if self.suggestedSpeaker != 0 :

						goAhead = self.func ("encourage")
						if goAhead :
							self.updateBelonginessRate(Speaker, "encourage")
							self.updateExplicit("encourage")
							#if self.firstround : self.func("startsession")


		if statusSpeech == "talking":

			t1 = round (speechduration % self.minspeech,1)
			# update speaking time half second, after the first 0.5 seconds assuming minspeech = 0.5
			if (t1 == 0.0) and (speechduration >= self.minspeech ) : # update each 2s todo 5Mar
				if Speaker != self.actualSpeaker :
					self.updateInterruptSpeakingTime(Speaker) #applied to organic and mediated
					#self.actualSpeaker = Speaker # Todo check 22fev
				self.increaseSpeakingTime (Speaker)
				if not self.organicspeech : self.updateSSspeakingTime(Speaker)

			triggerExp = round (speechduration % self.minspeech2move, 1)


			if (triggerExp == 0.0) and (speechduration >= self.minspeech2move)  : # x seconds minimium for checking new expression   eg 1.0

				print (f"statusSpeech {statusSpeech} duration state {durationstate} sugestedspeaker {self.suggestedSpeaker} speaker {Speaker} duration speech {speechduration} min speech {self.minspeech} time time {datetime.datetime.now()}  session duration {durationsession} ")

				self.actualSpeaker = Speaker # todo 22 fev
				# self.firstround = False # 8Mar
				if (self.state != statusSpeech) or (self.startState != startState):
					self.state = statusSpeech
					self.startState = startState
					self.logStates.append (( statusSpeech , startState, durationstate, self.grpID,  Speaker, self.suggestedSpeaker, self.organicspeech, self.startOrgSpeech, self.endOrgSpeech, self.startSuggestedUser, speechduration))




				goAheadEngage, goAheadTEmed, goAheadTEorganic, goAheadFollowing, goAheadEncourage,  goAheadFlwencourage, goAheadTE  = self.validateNextExpr (statusSpeech, Speaker, other_mic1ID, other_mic2ID, speechduration, atualtime)

				print ( f" ACT flags En : {goAheadEngage} TEM { goAheadTEmed} TEO {goAheadTEorganic}  TE {goAheadTE} Fw {goAheadFollowing} Enc {goAheadEncourage} Flen {goAheadFlwencourage}" )

				"""
				if self.lastround and (self.numlround < 3 ):
					if self.numlround == 0 :
						if self.organicspeech:
							self.organicspeech = False
							self.endOrgSpeech = atualtime

					self.validateNewSpeakerLastRound (self.numlround)
					if (self.newSpeaker != self.suggestedSpeaker):
						goAhead = self.func ("turnexchange")
						if goAhead :
							#self.te = 1 # mark ongoing TE
							self.updateSpeakerTE ()
							self.numlround += 1
							self.updateBelonginessRate(self.suggestedSpeaker, "turnexchange")
							self.updateExplicit("turnexchange")
					return
				"""

				if goAheadTE :
					self.validateNewSpeaker (self.counttime)
					if (self.newSpeaker != self.suggestedSpeaker):
						self.slowpace = (self.actualSpeaker == self.suggestedSpeaker)  and (speechduration >= self.minspeech2move*2) # 10MAr
						goAhead = self.func ("turnexchange")
						if goAhead :
							#self.te = 1 # mark ongoing TE
							self.updateSpeakerTE ()
							self.updateBelonginessRate(self.suggestedSpeaker, "turnexchange")
							self.updateExplicit("turnexchange")
					return

				if goAheadTEmed :
					self.validateNewSpeaker (self.counttime)
					self.startTEmedSpeech = atualtime
					self.organicspeech = False
					if (self.newSpeaker != self.suggestedSpeaker):
						self.slowpace = (self.actualSpeaker == self.suggestedSpeaker)  and (speechduration >= self.minspeech2move*2) #10 Mar
						goAhead = self.func ("turnorgmed")
						if goAhead :
							#self.te = 1 # mark ongoing TE
							self.updateSpeakerTE ()
							self.updateBelonginessRate(self.suggestedSpeaker, "turnorgmed")
							self.updateExplicit("turnorgmed")
					return

				if goAheadTEorganic :
					# todo add nonorganic period MUST DO
					self.organicspeech = True
					if self.suggestedSpeaker != 0 and self.teorganic == 0 : # 9Mar
						if Speaker != self.suggestedSpeaker:
							self.newSpeaker = Speaker
							self.slowpace = (self.actualSpeaker == self.suggestedSpeaker)  and (speechduration >= self.minspeech2move*2) #10 Mar
							goAhead = self.func ("teorganic")
							if goAhead :
								#self.te = 1 # mark ongoing TE
								self.updateSpeakerTE ()
								self.updateBelonginessRate(self.suggestedSpeaker, "teorganic")
								self.updateExplicit("teorganic")
							return
					"""
					else:
						if goAheadFlwencourage:
							goAhead = self.func("flwencourage") #reinforce flwencouragesuggested speaker
							if goAhead :
								self.updateBelonginessRate(Speaker, "flwencourage")
								self.updateExplicit("flwencourage")
							return

						if goAheadFollowing :
							goAhead = self.func("following") #todo validar se a resposta ao following é diferente
							if goAhead :
								self.updateBelonginessRate(Speaker, "following")
								self.updateExplicit("following")
							return
					

						if goAheadEngage :
							goAhead = self.func("engage")
							if goAhead : self.updateExplicit("engage")
							return
					"""
				if Speaker != self.suggestedSpeaker: # mudou o speaker

					# if self.p : print (f"ACT:  suggested {self.suggestedSpeaker} speaking {Speaker} , duration state {speechduration}")

					#self.actualSpeaker = Speaker

					if goAheadEncourage :
						goAhead = self.func("encourage") #todo validar se a resposta ao encourage  é diferente
						if goAhead :
							self.updateBelonginessRate(Speaker, "encourage")
							self.updateExplicit("encourage")
						return

					if goAheadFollowing :
						tempspeak = Speaker # 9Mar
						goAhead = self.func("following") #todo validar se a resposta ao following é diferente
						if goAhead :
							self.updateBelonginessRate(Speaker, "following")
							self.updateExplicit("following")
							if self.suggestedSpeaker == 0:
								self.newSpeaker = tempspeak
								self.updateSpeakerTE ()
								#self.firstround = False
						return

				else:
					if goAheadFlwencourage:
						goAhead = self.func("flwencourage") #reinforce flwencouragesuggested speaker
						if goAhead :
							self.updateBelonginessRate(Speaker, "flwencourage")
							self.updateExplicit("flwencourage")
						return

					if goAheadFollowing :
						goAhead = self.func("following") #todo validar se a resposta ao following é diferente
						if goAhead :
							self.updateBelonginessRate(Speaker, "following")
							self.updateExplicit("following")
						return


					if goAheadEngage :
						goAhead = self.func("engage")
						if goAhead : self.updateExplicit("engage")





	def updateExplicit(self, expressionID):

		if (expressionID == "turnexchange") or (expressionID == "turnorgmed") or (expressionID == "teorganic"):
			self.encourage = 0
			self.te = 0
			self.teorganic = 0
			self.flwencourage= 0
			self.following = 0
			self.explicit = False
			return

		if (expressionID == "following"):
			self.encourage = 0
			self.flwencourage= 0
			#self.te = 0
			if self.suggestedSpeaker == 0: self.teorganic = 0 #10MAr
			#if not overlap:
			self.following += 1
			#else: self.following = self.maxexpFollowTimes  #if overlap only Follow once
			self.explicit = False
			return

		if (expressionID == "encourage"):
			self.encourage +=1
			self.flwencourage= 0
			#self.te = 0
			self.following = 0
			self.explicit = (self.encourage >= self.maximpEncTimes)
			#self.explicit = not self.explicit
		elif expressionID == "flwencourage":
			self.flwencourage+= 1
			self.encourage = 0
			#self.te = 0
			self.following = 0
			self.explicit = (self.flwencourage >= self.maximpFlwTimes)
			#self.explicit = not self.explicit
		elif expressionID == "engage":
			self.engage += 1
		else:
			self.middle += 1





	def validateNextExpr (self, statusSpeech, Speaker, other_mic1ID, other_mic2ID, durationState, atualtime):

		#self.slowpace = self.checkBelonginessRateFlag(Speaker, other_mic1ID, other_mic2ID)
		#self.slowpace = (self.actualSpeaker == self.suggestedSpeaker)
		if self.condition == "baseline" :
			return False, False, False, False, False, False, False # Turn exchange on going
		if (self.te != 0) or (self.teorganic != 0)  :
			return False, False, False, False, False, False, False # Turn exchange on going
		print(f"ACT : VALIDATE NEXT EXPR : {statusSpeech} {Speaker} {other_mic1ID} {other_mic2ID} {durationState} enc numb {self.encourage}")

		if statusSpeech == "idle":

			triggerExpFollowing = 0.1 # no following in idle
			triggerExpEncourage = round (durationState % self.minidleencourage, 1)
			triggerExpflwencourage= 0.1  # no flwencouragein idle
			triggerExpEngage = 0.1

			triggerExpTE = 0.1
			triggerExpTEmed = 0.1
			triggerExpTEorganic = 0.1


			if self.condition == "followdriven" :
				"""
				if self.startOrgSpeech == -1 :
					triggerExpEngage = round (durationState % self.minidleengage, 1)# repeat start session
				else : triggerExpEngage = 0.1
				"""
				if (durationState > self.minidleTEorg) : # eg 25s
					triggerExpTEmed = 0.1 # eg 120 s
					if not self.organicspeech :
						self.startOrgSpeech = atualtime
						self.organicspeech = True
				elif self.encourage > (self.maxexpEncTimes + self.maximpEncTimes - 1): # force move to organic
					triggerExpTEmed = 0.1 # eg 120 s
					if not self.organicspeech :
						self.startOrgSpeech = atualtime
						self.organicspeech = True
			else:
				if (durationState > self.minidleTE) : # eg 45s
					triggerExpTE = 0.0
				if self.encourage > (self.maxexpEncTimes + self.maximpEncTimes - 1): # force TE
					triggerExpTE = 0.0


		else :
			triggerExpFollowing = round (durationState % self.minfollowing, 1) # eg 2s
			triggerExpEncourage = round (durationState % self.minencourage, 1) # eg 10 s
			triggerExpflwencourage= round (durationState % self.minflwencourage, 1) # eg 30 s
			triggerExpEngage = round (durationState % self.minengage, 1) # 2s
			triggerExpTEorganic = 0.1
			triggerExpTEmed = 0.1 # eg < 120 s
			triggerExpTE = 0.1 # eg < 120 s



			if self.condition == "followdriven" :
				triggerExpTEorganic = round (durationState % self.minTEorganic, 1) # eg 4s
				# organic follow condition
				if self.organicspeech : # if organic  mode evaluate the change to mediated mode
					# in organic speech time
					if self.startOrgSpeech == -1 : self.startOrgSpeech = atualtime
					durationOrgSpeech = atualtime - self.startOrgSpeech
					if (durationState > self.minTEorganic) and (self.teorganic == 0) :
						print(f" ACT : TEOrg duration  in Org speech  {durationOrgSpeech}")
						triggerExpTEorganic = 0.0 # todo avaliar se é isto 23fev



					if (durationOrgSpeech > self.minTEorgmed) and (self.teorganic == 0) :
						print(f" ACT : TEMed duration from Med change to Org speech  {durationOrgSpeech}")
						self.organicspeech = False
						self.endOrgSpeech = atualtime
						self.startSuggestedUser = atualtime
						self.startOrgSpeech = -1
						triggerExpTEmed = 0.0 # eg 120 s
						triggerExpTEorganic = 0.1

				else: # evaluate the change to organic mode
					# in mediated speech time
					durationSSpeaker = atualtime - self.startSuggestedUser
					if (durationSSpeaker > self.minTEorgnotmed) and (self.teorganic == 0): # move to organic mode
						self.organicspeech = True
						self.startOrgSpeech = atualtime
					print(f" ACT : TE duration from Med change to Org speech {durationSSpeaker}")
			else:
				# encouragedriven or control condition
				if self.encourage > (self.maxexpEncTimes + self.maximpEncTimes - 1 ):
					return False, False, False, False, False, False, True # Turn exchange
				durationSSpeaker = atualtime - self.startSuggestedUser
				if (durationSSpeaker > self.minTE) and (self.te == 0):  # move to new speaker
					triggerExpTE = 0.0 # eg 120 s
				print(f" ACT : TE duration SS Speaker {durationSSpeaker}")


			#if self.following >= self.maxexpFollowTimes: # number of times robot show following state
			#	triggerExpFollowing = 0.1



		#if self.p:

		print(f"ACT : VALIDATE NEXT EXPR TRIGGER {statusSpeech} {Speaker} Eg: {triggerExpEngage} Fl: {triggerExpFollowing} En: {triggerExpEncourage} FlEn : {triggerExpflwencourage}  TE: {triggerExpTE} TEO : {triggerExpTEorganic}")
		if (triggerExpTE == 0.0):
				#or ((triggerExpTE == self.minspeech2move) and (self.te == 0) and (durationState > self.minspeech2move)):
			# tolerance for 5 s to trigger TE movement
			return False, False, False, False, False, False, True

		if triggerExpTEorganic == 0.0 :
			return triggerExpEngage == 0.0, False, True, triggerExpFollowing == 0.0, triggerExpEncourage == 0.0, (triggerExpflwencourage== 0.0), False

		if triggerExpTEmed == 0.0 :
			return False, True, False, False, False, False, False

		if (triggerExpflwencourage== 0.0): # or ((triggerExpflwencourage== self.minspeech2move) and (durationState > self.minspeech2move)):
			# tolerance for 5 s to trigger TE movement
			return  False, False, False, False, False, True, False

		if triggerExpEncourage == 0.0 :
			return False, False, False, False, True, False, False

		if triggerExpFollowing == 0.0 :
			return False, False, False, True, False, False, False

		if triggerExpEngage == 0.0 :
			return True, False, False, False, False, False, False

		return False, False, False, False, False, False, False


	def checkBelonginessRateFlag(self, speaker1, speaker2, speaker3):

		if self.condition != "control":
			belongRateSP1 ,encR, teR, flwencR, followingR, teorgR, eR, mR  = self.returnBelonginessRate(speaker1)
			belongRateSP2, encR, teR, flwencR, followingR, teorgR, eR, mR  = self.returnBelonginessRate(speaker2)
			belongRateSP3,encR, teR, flwencR, followingR, teorgR, eR, mR = self.returnBelonginessRate(speaker3)
			#if self.p : print("ACT: belonginess rate speaker " + str(belongRateSP1) + " speaker 2: " + str(belongRateSP2) + " speaker 3: " + str(belongRateSP3))
			if (belongRateSP1 < belongRateSP2) and (belongRateSP1 < belongRateSP3):
				# least belonginess RAte child

				return True
			else:
				# not the least belonginess RAte child
				return False
		else:
			return False  # assume the some motivation to all participants


	def returnBelonginessRate (self, speakerID):
		if speakerID == self.speakerID1 :
			return self.belonginessRID1, self.encourageRID1, self.TERID1, self.flwencourageRID1, self.followingRID1, self.TEorgRID1, self.middleRID1, self.engageRID1
		if speakerID == self.speakerID2:
			return self.belonginessRID2, self.encourageRID2, self.TERID2, self.flwencourageRID2, self.followingRID2, self.TEorgRID2, self.middleRID2, self.engageRID2
		if speakerID == self.speakerID3 :
			return self.belonginessRID3,  self.encourageRID3, self.TERID3, self.flwencourageRID3, self.followingRID3, self.TEorgRID3, self.middleRID3, self.engageRID3

	def updateBelonginessRate (self, speakerID, expressionID):

		if speakerID == self.speakerID1 :
			if expressionID == "following":
				self.followingRID1 += 1.0
				return
			if expressionID == "middle":
				self.middleRID1 += 1.0
				return
			if expressionID == "engage":
				self.engageRID1 += 1.0
				return
			self.belonginessRID1 += 1.0
			if expressionID == "encourage":
				self.encourageRID1 += 1.0
			else:
				if (expressionID == "turnexchange") or (expressionID == "turnorgmed"):
					self.TERID1 += 1.0
				elif expressionID == "teorganic":
					self.TEorgRID1 += 1.0
				else: self.flwencourageRID1 += 1.0

		if speakerID == self.speakerID2 :
			if expressionID == "following":
				self.followingRID2 += 1.0
				return
			if expressionID == "middle":
				self.middleRID2 += 1.0
				return
			if expressionID == "engage":
				self.engageRID2 += 1.0
				return
			self.belonginessRID2 += 1.0
			if expressionID == "encourage":
				self.encourageRID2 += 1.0
			else:
				if (expressionID == "turnexchange") or (expressionID == "turnorgmed"):
					self.TERID2 += 1.0
				elif expressionID == "teorganic":
					self.TEorgRID2 += 1.0
				else:
					self.flwencourageRID2 += 1.0

		if speakerID == self.speakerID3 :
			if expressionID == "following":
				self.followingRID3 += 1.0
				return
			if expressionID == "middle":
				self.middleRID3 += 1.0
				return
			if expressionID == "engage":
				self.engageRID3 += 1.0
				return
			self.belonginessRID3 += 1.0
			if expressionID == "encourage":
				self.encourageRID3 += 1.0
			else:
				if (expressionID == "turnexchange") or (expressionID == "turnorgmed"):
					self.TERID3 += 1.0
				elif expressionID == "teorganic":
					self.TEorgRID3 += 1.0
				else:
					self.flwencourageRID3 += 1.0

	def updateInterruptSpeakingTime (self, speaker1):
		# record time child interrupted and was interrupted by
		if self.organicspeech : #when in organic speech
			# count time where the speaker interrupts others
			if speaker1 == self.speakerID1 : self.speakingInterruptTimeID1O += self.minspeech
			if speaker1 ==  self.speakerID2 : self.speakingInterruptTimeID2O += self.minspeech
			if speaker1 ==  self.speakerID3 : self.speakingInterruptTimeID3O += self.minspeech

			if self.actualSpeaker == self.speakerID1 : self.speakingInterruptedbyTimeID1O += self.minspeech
			if self.actualSpeaker ==  self.speakerID2 : self.speakingInterruptedbyTimeID2O += self.minspeech
			if self.actualSpeaker ==  self.speakerID3 : self.speakingInterruptedbyTimeID3O += self.minspeech
		else:
		# count time where the speaker interrupts others in mediated speech
			if speaker1 == self.speakerID1 : self.speakingInterruptTimeID1M += self.minspeech
			if speaker1 ==  self.speakerID2 : self.speakingInterruptTimeID2M += self.minspeech
			if speaker1 ==  self.speakerID3 : self.speakingInterruptTimeID3M += self.minspeech

			if self.actualSpeaker == self.speakerID1 : self.speakingInterruptedbyTimeID1M += self.minspeech
			if self.actualSpeaker ==  self.speakerID2 : self.speakingInterruptedbyTimeID2M += self.minspeech
			if self.actualSpeaker ==  self.speakerID3 : self.speakingInterruptedbyTimeID3M += self.minspeech

	def updateSSspeakingTime (self, speaker1):

		if self.suggestedSpeaker == speaker1 : # time spoke when the robot was near him (in mediated version)
			if speaker1 == self.speakerID1 : self.speakingSSinTimeID1 += self.minspeech
			if speaker1 ==  self.speakerID2 : self.speakingSSinTimeID2 += self.minspeech
			if speaker1 ==  self.speakerID3 : self.speakingSSinTimeID3 += self.minspeech
		else: # time spoke when the robot was away from him (in mediated version)
			if speaker1 == self.speakerID1 : self.speakingSSoutTimeID1 += self.minspeech
			if speaker1 ==  self.speakerID2 : self.speakingSSoutTimeID2 += self.minspeech
			if speaker1 ==  self.speakerID3 : self.speakingSSoutTimeID3 += self.minspeech



	def updateSpeakingTime (self, speaker1, speaker2, speaker3, speakingTime1, speakingTime2, speakingTime3):

		# update if the speaker is aligned with the suggested speaker (or is other)
		self.updateASpeakingTime (speaker1, speakingTime1)
		self.updateASpeakingTime (speaker2, speakingTime2)
		self.updateASpeakingTime (speaker3, speakingTime3)




	def updateASpeakingTime (self, speaker, speakingTime):
		# update the speaking time of each speaker
		if speaker == self.speakerID1 :
			self.speakingTimeID1 = speakingTime
		else :
			if speaker == self.speakerID2 :
				self.speakingTimeID2 = speakingTime
			else:
				self.speakingTimeID3 = speakingTime

	def increaseSpeakingTime (self, speaker):
		# update the speaking time organic or proposed by the robot of each speaker
		if speaker == self.speakerID1 :
			if self.organicspeech:
				self.speakingOrgTimeID1 += self.minspeech  # time spoked in organic
			else : self.speakingMedTimeID1 += self.minspeech # time spoked in mediated

		else :
			if speaker == self.speakerID2 :
				if self.organicspeech:
					self.speakingOrgTimeID2 += self.minspeech # time spoked in organic
				else : self.speakingMedTimeID2 += self.minspeech # time spoked in mediated
			else:
				if self.organicspeech:
					self.speakingOrgTimeID3 += self.minspeech # time spoked in organic
				else : self.speakingMedTimeID3 += self.minspeech # time spoked in mediated



	def validateNewSpeaker (self, sptime=False):
	# old organic

		if self.p:
			print ("ACT validate new speaker  Suggested Speaker " + str(self.suggestedSpeaker))

			print ("ACT ID1 Speaker " + str(self.speakerID1) + "time spoke 1: "+ str(self.speakingTimeID1))
			print ("ACT ID2 Speaker " + str(self.speakerID2) + "time spoke 2: "+ str(self.speakingTimeID2))
			print ("ACT ID3 Speaker " + str(self.speakerID3) + "time spoke 3: "+ str(self.speakingTimeID3))

		if not sptime :
			if self.suggestedSpeaker == self.speakerID1:
				sp1 =  self.speakerID1
				speakingTime1 = self.speakingTimeID1
				speakingTime2 = self.speakingTimeID2
				sp2 = self.speakerID2
				speakingTime3 = self.speakingTimeID3
				sp3 = self.speakerID3

			elif self.suggestedSpeaker == self.speakerID2:
				sp1 =  self.speakerID2
				speakingTime1 = self.speakingTimeID2
				speakingTime2 = self.speakingTimeID1
				sp2 = self.speakerID1
				speakingTime3 = self.speakingTimeID3
				sp3 = self.speakerID3

			else:
				sp1 =  self.speakerID3
				speakingTime1 = self.speakingTimeID3

				speakingTime2 = self.speakingTimeID1
				sp2 = self.speakerID1
				speakingTime3 = self.speakingTimeID2
				sp3 = self.speakerID2
		else:
			if self.suggestedSpeaker == self.speakerID1:
				sp1 =  self.speakerID1
				speakingTime1 = self.speakingOrgTimeID1 + self.speakingMedTimeID1
				speakingTime2 = self.speakingOrgTimeID2 + self.speakingMedTimeID2
				sp2 = self.speakerID2
				speakingTime3 = self.speakingOrgTimeID3 + self.speakingMedTimeID3
				sp3 = self.speakerID3

			elif self.suggestedSpeaker == self.speakerID2:
				sp1 =  self.speakerID2
				speakingTime1 = self.speakingOrgTimeID2 + self.speakingMedTimeID2
				speakingTime2 = self.speakingOrgTimeID1 + self.speakingMedTimeID1
				sp2 = self.speakerID1
				speakingTime3 = self.speakingOrgTimeID3 + self.speakingMedTimeID3
				sp3 = self.speakerID3

			else:
				sp1 =  self.speakerID3
				speakingTime1 = self.speakingOrgTimeID3 + self.speakingMedTimeID3

				speakingTime2 = self.speakingOrgTimeID1 + self.speakingMedTimeID1
				sp2 = self.speakerID1
				speakingTime3 = self.speakingOrgTimeID2 + self.speakingMedTimeID2
				sp3 = self.speakerID2

		if self.condition == "control":
			# if control or timesp2 = timesp3
			listspeakers = []
			listspeakers.append (sp2)
			listspeakers.append (sp3)
			nextSpeaker = random.choice(listspeakers)
			self.newSpeaker = nextSpeaker
		elif self.condition == "encouragedriven":
			if speakingTime2 < speakingTime3 : self.newSpeaker = sp2
			else: self.newSpeaker = sp3
		else:
			if speakingTime1 < speakingTime2:
				if speakingTime1 < speakingTime3 : self.newSpeaker = sp1
				else: self.newSpeaker = sp3
			else:
				if speakingTime2 < speakingTime3 : self.newSpeaker = sp2
				else: self.newSpeaker = sp3

	def validateNewSpeakerLastRound (self, num):
		# last round, move across all speakers from most to least participative

		if self.numlround == 0:
			if self.p:
				print ("ACT validate new speaker last round Suggested Speaker " + str(self.suggestedSpeaker))

				print ("ACT ID1 Speaker " + str(self.speakerID1) + "time spoke 1: "+ str(self.speakingTimeID1))
				print ("ACT ID2 Speaker " + str(self.speakerID2) + "time spoke 2: "+ str(self.speakingTimeID2))
				print ("ACT ID3 Speaker " + str(self.speakerID3) + "time spoke 3: "+ str(self.speakingTimeID3))


			if (self.speakingTime1 >= self.speakingTime2) and  (self.speakingTime1 >= self.speakingTime3) :
				if self.speakingTime2 >= self.speakingTime3 :
					self.lastround  = [self.speakerID1, self.speakerID2, self.speakerID3]
				else:
					self.lastround  = [self.speakerID1, self.speakerID3, self.speakerID2]

			if (self.speakingTime2 >= self.speakingTime1) and  (self.speakingTime2 >= self.speakingTime3) :
				if self.speakingTime1 >= self.speakingTime3 :
					self.lastround  = [self.speakerID2, self.speakerID1, self.speakerID3]
				else:
					self.lastround  = [self.speakerID2, self.speakerID3, self.speakerID1]

			if (self.speakingTime3 >= self.speakingTime1) and  (self.speakingTime3 >= self.speakingTime3) :
				if self.speakingTime1 >= self.speakingTime2 :
					self.lastround  = [self.speakerID3, self.speakerID1, self.speakerID2]
				else:
					self.lastround  = [self.speakerID3, self.speakerID2, self.speakerID1]

		self.newSpeaker =  self.lastround[self.numlround]


	def updateSpeakerTE (self):
	# todo uma gralha o next speaker é atualizado no ultimo TE
		print("ACT : update suggested Speaker from : " + str(self.suggestedSpeaker)  + " to: " +  str(self.newSpeaker))
		if self.organicspeech :
			self.logSpeaker.append (( self.organicspeech, time.time(), self.grpID, self.newSpeaker,self.actualSpeaker, self.suggestedSpeaker))
			#self.actualSpeaker = self.newSpeaker
			self.suggestedSpeaker = self.newSpeaker
			self.startSuggestedUser = time.time()
			self.newSpeaker = 0


		elif self.suggestedSpeaker != self.newSpeaker :
			self.startSuggestedUser = time.time()
			self.logSpeaker.append (( self.organicspeech, self.startSuggestedUser, self.grpID, self.newSpeaker,self.actualSpeaker, self.suggestedSpeaker))
			self.suggestedSpeaker = self.newSpeaker
			self.actualSpeaker = self.suggestedSpeaker # 2602
			self.newSpeaker = 0



	#===============================================================================
	#
	#                              ROBOT Expression
	#
	#===============================================================================

	def func(self, expression):
		if (self.condition == "baseline") or (self.robot.dash.is_connected == False)  : return False

		goAhead = self.registerExpression(expression, self.explicit)
		# print (f"condition {self.condition}")


		#DOUBLE-CLICK
		if expression == "end":
			while goAhead == False:
				print("ACT: tried to end but robot is still doing stuff")
				time.sleep(1)
				print("ACT: next try ")
				goAhead = self.registerExpression(expression, self.explicit)
				#endingLoop = asyncio.new_event_loop()

			sp1N = self.checkName(self.speakerID1)
			sp2N = self.checkName(self.speakerID2)
			sp3N = self.checkName(self.speakerID3)



			if self.suggestedSpeaker == self.speakerID1:
				self.robot.executeExpression(expression, self.speakerID1, sp1N, self.speakerID2, sp2N, self.speakerID3, sp3N, self.slowpace,self.lastround,self.explicit)
			elif self.suggestedSpeaker == self.speakerID2:
				self.robot.executeExpression(expression, self.speakerID2, sp2N, self.speakerID1, sp1N, self.speakerID3, sp3N, self.slowpace, self.lastround,self.explicit)
			else :
				self.robot.executeExpression(expression, self.speakerID3, sp3N, self.speakerID2, sp2N, self.speakerID1, sp1N, self.slowpace,self.lastround, self.explicit)


			if self.p : print("ACT: played expression : " + expression)
			#now = datetime.datetime.now()

			self.finishActivity()

		else:

			if goAhead:
				if (expression == "turnexchange") : self.te = 1
				if (expression  == "teorganic") : self.teorganic = 1
				if (expression == "turnorgmed"): self.te = 1
				if (expression == "firstspeaker") :
					self.startSuggestedUser = time.time() # start the time
					#self.te = 1
				if (expression == "following") and (self.suggestedSpeaker == 0): # 10Mar
					self.teorganic = 1 # 10Mar

				#expressionLoop = asyncio.new_event_loop()
				actualSpeakername = self.checkName(self.actualSpeaker)
				newSpeakername = self.checkName(self.newSpeaker)
				suggestedSpeakername = self.checkName(self.suggestedSpeaker)

				if self.condition == "encouragedriven":
					print("ACT: Encourage driven condition "  + ", " + str(self.count) + " expression " + expression + " explicit " + str(self.explicit))
					self.robot.executeExpression(expression, self.suggestedSpeaker, suggestedSpeakername, self.actualSpeaker, actualSpeakername, self.newSpeaker, newSpeakername, self.slowpace, self.organicspeech,self.explicit)
					self.count = self.count + 1
				elif self.condition == "control":
					print("ACT: Control condition " + ", " + str(self.count) +
						  "expression " + expression + " explicit" + str(self.explicit))
					self.robot.executeExpression(expression, self.suggestedSpeaker, suggestedSpeakername, self.actualSpeaker, actualSpeakername, self.newSpeaker, newSpeakername, self.slowpace, self.organicspeech,self.explicit)
					self.count = self.count + 1
				elif self.condition == "followdriven":
					print("ACT: Follow driven follow condition " + ", " + str(self.count) +
						  "expression " + expression + " explicit" + str(self.explicit))
					self.robot.executeExpression(expression, self.suggestedSpeaker, suggestedSpeakername, self.actualSpeaker, actualSpeakername, self.newSpeaker, newSpeakername, self.slowpace, self.organicspeech, self.explicit)
					self.count = self.count + 1


				if self.p : print("ACT: played expression : " + expression )

		return goAhead


	def registerExpression(self, expressionID, explicit):
		#Register all button presses, even those who did nothing
		now = datetime.datetime.now()

		goAhead = True

		goAhead = self.checkRobotBehavior(expressionID, now)

		if (expressionID == "turnexchange") or (expressionID == "turnorgmed") :
			if self.te == 1 :
				goAhead = False
			elif goAhead == True :
				self.te = 1

		if (expressionID == "teorganic"):
			if self.teorganic == 1 :
				goAhead = False
			elif goAhead == True :
				self.teorganic = 1

		if (expressionID != "lastminute"):
			self.logExpression.append((expressionID, explicit, now, goAhead, self.grpID, self.suggestedSpeaker, self.startSuggestedUser, self.actualSpeaker, self.newSpeaker, self.state, self.startState,self.organicspeech,

								   (self.speakerID1, self.childID1,
								   self.speakingTimeID1, self.speakingInterruptTimeID1M, self.speakingInterruptedbyTimeID1M, self.speakingInterruptTimeID1O, self.speakingInterruptedbyTimeID1O,
								   self.speakingSSinTimeID1, self.speakingSSoutTimeID1, self.speakingOrgTimeID1, self.speakingMedTimeID1,
								   self.followingRID1, 	self.TEorgRID1, self.encourageRID1, self.TERID1, self.flwencourageRID1, self.belonginessRID1, self.middleRID1, self.engageRID1),


								   (self.speakerID2, self.childID2,
								   self.speakingTimeID2, self.speakingInterruptTimeID1M, self.speakingInterruptedbyTimeID2M,self.speakingInterruptTimeID2O, self.speakingInterruptedbyTimeID2O,
								   self.speakingSSinTimeID2, self.speakingSSoutTimeID2,self.speakingOrgTimeID2,self.speakingMedTimeID2,
								   self.followingRID2, self.TEorgRID2, self.encourageRID2, self.TERID2, self.flwencourageRID2, self.belonginessRID2, self.middleRID2, self.engageRID2),

								   (self.speakerID3, self.childID3,
								   self.speakingTimeID3, self.speakingInterruptTimeID3M, self.speakingInterruptedbyTimeID3M, self.speakingInterruptTimeID3O, self.speakingInterruptedbyTimeID3O,
								   self.speakingSSinTimeID3, self.speakingSSoutTimeID3, self.speakingOrgTimeID3, self.speakingMedTimeID3,
								   self.followingRID3, self.TEorgRID3,self.encourageRID3, self.TERID3, self.flwencourageRID3, self.belonginessRID3, self.middleRID3, self.engageRID3)


								   ))


			print("\nACT: state activated : " + str(self.state) + " expression activated: " + str(expressionID) + " " + str(now))
			print("ACT: Suggested Speaker : " + str(self.suggestedSpeaker)  + " Atual Speaker : " + str(self.actualSpeaker) + " New Speaker : " + str(self.newSpeaker))
			print("ACT: expression : " + str(expressionID) + " goAhead: " + str(goAhead))

		return goAhead



	def checkRobotBehavior(self, expression, presentTime):

		if self.p: print("ACT: checking if i can go")
		#goAhead = False validar
		goAhead = True
		if len(self.logExpression) > 1:
			for (e,eb, t,g, ssp, grp, stssp, ap1,np2,s , sts, orgs, sp1, sp2, sp3) in reversed(self.logExpression):
				if e != "end":
					if g == True: break
			prev_expression = e
			print ("Prev expression " + e)
			before = self.activatedExpression[prev_expression]
			delta = presentTime - before

			#if condition == "encouragedriven": okTime = checkExpressionTime(prev_expression)
			#elif condition == "control": okTime = checkNeutralTime()

			okTime = self.checkExpressionTime(prev_expression, eb)
			print ("ACT: check expression time " + str(okTime) + " versus time done" + str(delta.total_seconds()))
			if delta.total_seconds() > okTime:

				if self.p: print ("ACT: check expression time " + str(okTime) + "versus time done" + str(delta.total_seconds()))
				goAhead = True
			else:
				goAhead = False

		if goAhead : self.activatedExpression[expression] = presentTime
		return goAhead


	def warninglastminute (self):

		goAhead = False
		goAhead = self.func ("lastminute")
		if not goAhead : self.robot.dash.say ("my1")



	def warningstart (self):


		goAhead = self.func ("startsession")



#===============================================================================
#
#                             CONFIGURATIONS
#
#===============================================================================

	def checkExpressionTime(self, expression, explicit):
		if expression == "firstspeaker" :
			if explicit:
				return 7.5 # 5Mar 8 # 7.5
			else:
				return 4.2 # 5Mar 5 # 4.2 #  explicito (7.2-8.	02 1 phrase ou 4.06-4.9 ph + name )  implicit : 5.27

		elif expression == "turnexchange" :
			if explicit:
				return 10 # 9.5
			else:
				return 10 # 5Mar 8 # 7.5 #  explicito (nax 9.09-10.09 )  implicit : 7.3-8.2 1vez organic 7.33

		elif expression == "teorganic" :
			if explicit:
				return 10 # 9.1
			else:
				return 10 # 5Mar 88 # 7.43 #  explicito (9.7 - 10.3)  implicit : 7.3-8.0 1vez organic 6.02

		elif expression == "turnorgmed" : #equal to TE
			if explicit:
				return 10 # 9.5
			else:
				return 8 # 7.3 #  explicito (nax 9.84 )  implicit : 7.3 1vez organic 7.33

		elif expression == "middle" : return 3 # 2.7
		elif expression == "following" :
			return 2.0 # 2.5 #  0.2 used to allow low for 2.5s to the speaker

		elif expression == "encourage":
			if explicit:
				return 8 # 7.69
			else: return 6.5 # 5.27 #  explicito (5.78 1 phrase ou 7.69 ph + name )  implicit : 5.27
		elif expression == "flwencourage" :
			if explicit:
				return 4 # 3.4
			else: return 2 # 1.4 #  explicito (5.78 1 phrase ou 7.69 ph + name )  implicit : 5.27
		elif expression == "end": return 5 # 5.28  # 5.28

		elif expression == "engage": return 2 # 1.71 # 1.71
		elif expression == "lastminute" : return 2 # 1.71
		elif expression == "startsession" : return  1.71


	def checkName(self, speaker):


		if speaker == self.speakerID1: # name1
			return self.name1
		if speaker == self.speakerID2: # name2
			return self.name2
		if speaker == self.speakerID3: # name3
			return self.name3
		if speaker == self.organicID:
			if self.actualSpeaker != 0 : return self.checkName(self.actualSpeaker)
			else:	return ""





	def updateTimePerExpression(self, expresssion, now): # avaliar se é necessário ou apagar

		if self.previousState == "empty":
			previousRoom = expression
			logTotalTimePerRoom[emotion] = now
		else:
			if previousRoom != emotion:
				#	if emotion not in logTimePerRoom.keys():
				delta = now - logTotalTimePerRoom[previousRoom]
				logTotalTimePerRoom[previousRoom] = delta
				logTotalTimePerRoom[emotion] = now
				if previousRoom in logTotalTimePerRoom.keys():
					delta = now - activatedButtons[previousRoom]
					logTotalTimePerRoom[previousRoom] = logTotalTimePerRoom[previousRoom] + delta
				previousRoom = emotion

	def printActMetrics(self):
		print("Activity metrics")
		print("group_id {}".format(self.grpID))
		print("speaker_id 1 {}".format(self.speakerID1))
		print("child id 1 {}".format(self.childID1))
		print("speaking time {}".format(self.speakingTimeID1))
		print("speaking Interrupted by id 1 med speech {}".format(self.speakingInterruptTimeID1M))
		print("speaking id 1 Interrupted by others med speech  {}".format(self.speakingInterruptedbyTimeID1M))
		print("speaking Interrupted by id 1 in organic speech {}".format(self.speakingInterruptTimeID1O))
		print("speaking id 1 Interrupted by others  {} in organic speech ".format(self.speakingInterruptedbyTimeID1O))
		print("speaking id 1 when SS  {}".format(self.speakingSSinTimeID1))
		print("speaking id 1 when not SS  {}".format(self.speakingSSoutTimeID1))
		print("speaking id 1 when org  {}".format(self.speakingOrgTimeID1))
		print("speaking id 1 when med  {}".format(self.speakingMedTimeID1))

		print("belonginess rate  1 {}".format(self.belonginessRID1))
		print("following rate  1 {}".format(self.followingRID1))
		print("TE org rate 1 {}".format(self.TEorgRID1))
		print("encourage rate  1 {}".format(self.encourageRID1))
		print("TE rate  1 {}".format(self.TERID1))
		print("flwencourage rate 1  {}".format(self.flwencourageRID1))
		print("Engage rate 1 {}".format(self.engageRID1))
		print("Middle rate  1 {}".format(self.middleRID1))



		print("speaker_id 2 {}".format(self.speakerID2))
		print("child id 2 {}".format(self.childID2))
		print("speaking time {}".format(self.speakingTimeID2))
		print("speaking Interrupted by id 2 med speech {} ".format(self.speakingInterruptTimeID2M))
		print("speaking id 2 Interrupted by others med speech  {}".format(self.speakingInterruptedbyTimeID2M))
		print("speaking Interrupted by id 1 in organic speech{}".format(self.speakingInterruptTimeID2O))
		print("speaking id 1 Interrupted by others  {} in organic speech ".format(self.speakingInterruptedbyTimeID2O))

		print("speaking id 2 when SS  {}".format(self.speakingSSinTimeID2))
		print("speaking id 2 when not SS  {}".format(self.speakingSSoutTimeID2))
		print("speaking id 2 when org  {}".format(self.speakingOrgTimeID2))
		print("speaking id 2 when med  {}".format(self.speakingMedTimeID2))
		print("belonginess rate 2  {}".format(self.belonginessRID2))
		print("following rate 2  {}".format(self.followingRID2))
		print("TE org rate  2 {}".format(self.TEorgRID2))
		print("encourage rate  2 {}".format(self.encourageRID2))
		print("TE rate  2 {}".format(self.TERID2))
		print("flwencourage rate  2 {}".format(self.flwencourageRID2))
		print("Engage rate 2 {}".format(self.engageRID2))
		print("Middle rate  2 {}".format(self.middleRID2))


		print("speaker_id 3 {}".format(self.speakerID3))
		print("child id 3 {}".format(self.childID3))
		print("speaking time {}".format(self.speakingTimeID3))
		print("speaking Interrupted by id 3 med speech {}".format(self.speakingInterruptTimeID3M))
		print("speaking id 3 Interrupted by others med speech  {}".format(self.speakingInterruptedbyTimeID3M))
		print("speaking Interrupted by id 1 in organic speech{}".format(self.speakingInterruptTimeID3O))
		print("speaking id 1 Interrupted by others  {} in organic speech ".format(self.speakingInterruptedbyTimeID3O))
		print("speaking id 3 when SS  {}".format(self.speakingSSinTimeID3))
		print("speaking id 3 when not SS  {}".format(self.speakingSSoutTimeID3))
		print("speaking id 3 when org  {}".format(self.speakingOrgTimeID3))
		print("speaking id 3 when med  {}".format(self.speakingMedTimeID3))
		print("belonginess rate 3 {}".format(self.belonginessRID3))
		print("following rate 3  {}".format(self.followingRID3))
		print("TE org rate  3 {}".format(self.TEorgRID3))
		print("encourage rate  3 {}".format(self.encourageRID3))
		print("TE rate  3 {}".format(self.TERID3))
		print("flwencourage rate 3 {}".format(self.flwencourageRID3))
		print("Engage rate 3 {}".format(self.engageRID3))
		print("Middle rate  3 {}".format(self.middleRID3))

	def logActMetrics(self):
		activity_logs = []

		log_directory = f"logs/{self.condition}/{self.grpID}/"

		pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)


		file = log_directory + f"/ACT_logs_{self.grpID}_{self.startTime}.log"
		logging.basicConfig(filename=file, level=logging.DEBUG)
		logging.info("====== starttime   ======")
		logging.info(str(self.startTime))
		logging.info("====== condition  ======")
		logging.info(str(self.condition))
		logging.info("====== group  ======")
		logging.info(str(self.grpID))


		logging.info("======SPEAKER 1 ======")
		logging.info(str(self.speakerID1))
		logging.info("======CHILD 1 ======")
		logging.info(str(self.childID1))
		logging.info("======Speaking Time ======")
		logging.info(str(self.speakingTimeID1))
		logging.info("======Speaking Interrupted Count sec med speech  ======")
		logging.info(str(self.speakingInterruptTimeID1M))
		logging.info("======Speaking Interruted by others Count sec med speech======")
		logging.info(str(self.speakingInterruptedbyTimeID1M))
		logging.info("======Speaking Interrupted Count in organic speech ======")
		logging.info(str(self.speakingInterruptTimeID1O))
		logging.info("======Speaking Interruted by others Count in organic speech======")
		logging.info(str(self.speakingInterruptedbyTimeID1O))

		logging.info("======speaking id 1 when SS ======")
		logging.info(str(self.speakingSSinTimeID1))
		logging.info("======speaking id 1 when not SS  ======")
		logging.info(str(self.speakingSSoutTimeID1))
		logging.info("======speaking id 1 when org  ======")
		logging.info(str(self.speakingOrgTimeID1))
		logging.info("======speaking id 1 when med  ======")
		logging.info(str(self.speakingMedTimeID1))

		logging.info("=====Belonginess 1 ======")
		logging.info(str(self.belonginessRID1))
		logging.info("=====following 1 ======")
		logging.info(str(self.followingRID1))
		logging.info("===== TE org 1 ======")
		logging.info(str(self.TEorgRID1))
		logging.info("=====Encourage 1 ======")
		logging.info(str(self.encourageRID1))
		logging.info("===== TE 1 ======")
		logging.info(str(self.TERID1))
		logging.info("=====flwencourage  1 ======")
		logging.info(str(self.flwencourageRID1))
		logging.info("===== engage 1 ======")
		logging.info(str(self.engageRID1))
		logging.info("=====middle  1 ======")
		logging.info(str(self.middleRID1))


		logging.info("======SPEAKER 2 ======")
		logging.info(str(self.speakerID2))
		logging.info("======CHILD 2 ======")
		logging.info(str(self.childID2))
		logging.info("======Speaking Time ======")
		logging.info(str(self.speakingTimeID2))
		logging.info("======Speaking Interrupted Count med speech======")
		logging.info(str(self.speakingInterruptTimeID2M))
		logging.info("======Speaking Interruted by others Count ======")
		logging.info(str(self.speakingInterruptedbyTimeID2M))
		logging.info("======Speaking Interrupted Count in organic speech ======")
		logging.info(str(self.speakingInterruptTimeID2O))
		logging.info("======Speaking Interruted by others Count in organic speech======")
		logging.info(str(self.speakingInterruptedbyTimeID2O))

		logging.info("======speaking id 2 when SS ======")
		logging.info(str(self.speakingSSinTimeID2))
		logging.info("======speaking id 2 when not SS  ======")
		logging.info(str(self.speakingSSoutTimeID2))
		logging.info("======speaking id 2 when org  ======")
		logging.info(str(self.speakingOrgTimeID2))
		logging.info("======speaking id 1 when med  ======")
		logging.info(str(self.speakingMedTimeID2))

		logging.info("=====Belonginess 2 ======")
		logging.info(str(self.belonginessRID2))
		logging.info("=====following 2 ======")
		logging.info(str(self.followingRID2))
		logging.info("===== TE org 2 ======")
		logging.info(str(self.TEorgRID2))
		logging.info("=====Encourage 2 ======")
		logging.info(str(self.encourageRID2))
		logging.info("===== TE 2 ======")
		logging.info(str(self.TERID2))
		logging.info("=====flwencourage 2 ======")
		logging.info(str(self.flwencourageRID2))
		logging.info("===== engage 2 ======")
		logging.info(str(self.engageRID2))
		logging.info("=====middle  2 ======")
		logging.info(str(self.middleRID2))

		logging.info("======SPEAKER 3======")
		logging.info(str(self.speakerID3))
		logging.info("======CHILD 3 ======")
		logging.info(str(self.childID3))
		logging.info("======Speaking Time ======")
		logging.info(str(self.speakingTimeID3))
		logging.info("======Speaking Interrupted Count med speech======")
		logging.info(str(self.speakingInterruptTimeID3M))
		logging.info("======Speaking Interruted by others Count med speech ======")
		logging.info(str(self.speakingInterruptedbyTimeID3M))
		logging.info("======Speaking Interrupted Count in organic speech ======")
		logging.info(str(self.speakingInterruptTimeID3O))
		logging.info("======Speaking Interruted by others Count in organic speech======")
		logging.info(str(self.speakingInterruptedbyTimeID3O))

		logging.info("======speaking id 3 when SS ======")
		logging.info(str(self.speakingSSinTimeID3))
		logging.info("======speaking id 3 when not SS  ======")
		logging.info(str(self.speakingSSoutTimeID3))
		logging.info("======speaking id 3 when org  ======")
		logging.info(str(self.speakingOrgTimeID3))
		logging.info("======speaking id 1 when med  ======")
		logging.info(str(self.speakingMedTimeID3))

		logging.info("=====Belonginess 3 ======")
		logging.info(str(self.belonginessRID3))
		logging.info("=====following 3 ======")
		logging.info(str(self.followingRID3))
		logging.info("===== TE org 3 ======")
		logging.info(str(self.TEorgRID3))
		logging.info("=====Encourage 3======")
		logging.info(str(self.encourageRID3))
		logging.info("===== TE 3 ======")
		logging.info(str(self.TERID3))
		logging.info("=====flwencourage ======")
		logging.info(str(self.flwencourageRID3))
		logging.info("===== engage 3 ======")
		logging.info(str(self.engageRID3))
		logging.info("=====middle  3 ======")
		logging.info(str(self.middleRID3))
		# logs

		activity_logs.append(str(self.speakerID1))
		activity_logs.append(str(self.grpID))
		activity_logs.append(str(self.childID1))
		activity_logs.append(str(self.speakingTimeID1))
		activity_logs.append(str(self.speakingInterruptTimeID1M))
		activity_logs.append(str(self.speakingInterruptedbyTimeID1M))
		activity_logs.append(str(self.speakingInterruptTimeID1O))
		activity_logs.append(str(self.speakingInterruptedbyTimeID1O))
		activity_logs.append(str(self.speakingSSinTimeID1))
		activity_logs.append(str(self.speakingSSoutTimeID1))
		activity_logs.append(str(self.speakingOrgTimeID1))
		activity_logs.append(str(self.speakingMedTimeID1))

		activity_logs.append(str(self.belonginessRID1))
		activity_logs.append(str(self.followingRID1))
		activity_logs.append(str(self.TEorgRID1))
		activity_logs.append(str(self.encourageRID1))
		activity_logs.append(str(self.TERID1))
		activity_logs.append(str(self.flwencourageRID1))
		activity_logs.append(str(self.engageRID1))
		activity_logs.append(str(self.middleRID1))



		activity_logs.append(str(self.speakerID2))
		activity_logs.append(str(self.grpID))
		activity_logs.append(str(self.childID2))
		activity_logs.append(str(self.speakingTimeID2))
		activity_logs.append(str(self.speakingInterruptTimeID2M))
		activity_logs.append(str(self.speakingInterruptedbyTimeID2M))
		activity_logs.append(str(self.speakingInterruptTimeID2O))
		activity_logs.append(str(self.speakingInterruptedbyTimeID2O))
		activity_logs.append(str(self.speakingSSinTimeID2))
		activity_logs.append(str(self.speakingSSoutTimeID2))
		activity_logs.append(str(self.speakingOrgTimeID2))
		activity_logs.append(str(self.speakingMedTimeID2))

		activity_logs.append(str(self.belonginessRID2))
		activity_logs.append(str(self.followingRID2))
		activity_logs.append(str(self.TEorgRID2))
		activity_logs.append(str(self.encourageRID2))
		activity_logs.append(str(self.TERID2))
		activity_logs.append(str(self.flwencourageRID2))
		activity_logs.append(str(self.engageRID2))
		activity_logs.append(str(self.middleRID2))


		activity_logs.append(str(self.speakerID3))
		activity_logs.append(str(self.grpID))
		activity_logs.append(str(self.childID3))
		activity_logs.append(str(self.speakingTimeID3))
		activity_logs.append(str(self.speakingInterruptTimeID3M))
		activity_logs.append(str(self.speakingInterruptedbyTimeID3M))
		activity_logs.append(str(self.speakingInterruptTimeID3O))
		activity_logs.append(str(self.speakingInterruptedbyTimeID3O))
		activity_logs.append(str(self.speakingSSinTimeID3))
		activity_logs.append(str(self.speakingSSoutTimeID3))
		activity_logs.append(str(self.speakingOrgTimeID3))
		activity_logs.append(str(self.speakingMedTimeID3))

		activity_logs.append(str(self.belonginessRID3))
		activity_logs.append(str(self.followingRID3))
		activity_logs.append(str(self.TEorgRID3))
		activity_logs.append(str(self.encourageRID3))
		activity_logs.append(str(self.TERID3))
		activity_logs.append(str(self.flwencourageRID3))
		activity_logs.append(str(self.engageRID3))
		activity_logs.append(str(self.middleRID3))


		return activity_logs

#===============================================================================
#
#                                   MAIN
#
#===============================================================================

