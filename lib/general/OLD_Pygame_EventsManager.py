import sys, pygame
import logging


class EventsManager():
	eventCallBacksList = []
	
	def __init__(self):
		pass
	
	def registerCallBack(self, eventType, callBackFunction):
		if eventType == "ALL_KEY_MOUSE_EVENTS" :
			self.eventCallBacksList.append([pygame.MOUSEBUTTONDOWN,callBackFunction])
			self.eventCallBacksList.append([pygame.MOUSEBUTTONUP,callBackFunction])
			self.eventCallBacksList.append([pygame.MOUSEMOTION,callBackFunction])
			self.eventCallBacksList.append([pygame.KEYDOWN,callBackFunction])
			self.eventCallBacksList.append([pygame.KEYUP,callBackFunction])
		else:
			self.eventCallBacksList.append([eventType,callBackFunction])
	
	
	def processEventsQueue(self):
		for event in pygame.event.get():	#loop through events
			
			for callBack in self.eventCallBacksList:	#loop through callbacks
				if callBack[0] == event.type:			# if call back type matches event type, call the callback function
					callBack[1](event)
				

