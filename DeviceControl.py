# coding: utf-8

from firebase.firebase import FirebaseApplication

import threading
import dwf
import datetime, time
import ast

import copy

class DeviceControl():
	global firebase

	def __init__(self):
		self.firebase_address = "https://qttest0513.firebaseio.com/"
		self.tryCount = 0
		self.dataCounter = 0
		self.getData = 0
		self.command = 0
		self.checkMeasureTime = 0
		self.deviceState = "ready"
		self.pauseFlag = False
		self.setupData = {
			'channels': 0,
			'freqs': 0,
			'interval': 0,
			'deadline': 0,
			'experiment_name': 0,
		}

		dwf.initialize()
		self.initFirebase()

	"""
	firebase에 접속하고 변수에 담아줌
	"""
	def connectFirebase(self):
		global firebase

		print("firebase connection")
		firebase = FirebaseApplication(self.firebase_address)
		self.tryCount = 0

	"""
	Firebase의 '/CONTROL' 초기화
	"""
	def initFirebase(self):
		global firebase

		print(" ### Firebase initializing")
		self.connectFirebase()

		CONTROL = {
			'COMMAND': 0,
			'DEVICESTATE': 'ready',
			'SETUP': 0,
			'PAUSE': False,
		}
		firebase.put('/CONTROL', '/', CONTROL)

		print(" ### Init complete")


	def monitorCommand(self):
		# global firebase
		# global getData

		while(True):
			try:
				self.getData = firebase.get('/CONTROL', None)
			except Exception as e:
				print("firebase connection error.. retry")
				self.connectFirebase()
				self.monitorCommand()

			self.command = self.getData['COMMAND']
			self.pauseFlag = self.getData['PAUSE']

			# command check
			if (self.command == 'checkchip'):
				print("!! CHECKCHIP command received")
				result = dwf.checkChip()
				firebase.put('/CHECKCHIP', '/', result)

			elif (self.command == 'setup'):
				if (self.deviceState == 'ready' or self.deviceState == 'setup'):
					print("!! SETUP command received")
					self.setupData = copy.deepcopy(self.getData['SETUP'])
					self.setupData['channels'] = ast.literal_eval(self.setupData['channels'])
					self.setupData['freqs'] = ast.literal_eval(self.setupData['freqs'])

					self.deviceState = 'setup'
					firebase.put('/' + self.setupData['experiment_name'], '/setup/', self.setupData)

					print("setup data : ", self.setupData)
				else:
					print("device not ready")

			elif (self.command == 'start'):
				print("!! START command received")
				now = datetime.datetime.now()

				self.deviceState = 'running'
				self.dataCounter = 0

			elif (self.command == 'stop'):
				# measurement 중지시키고 파이어베이스 초기화해야됨
				print("!! STOP command received")

				self.initFirebase()
				self.deviceState = "ready"

			elif (self.command == 'pause'):
				print("!! PAUSE command received")
				self.pauseFlag = True
				self.deviceState = "pause"

				print("#### DEVICE PAUSE")

			elif (self.command == 'unpause'):
				print("!! UNPAUSE command received")
				self.pauseFlag = False
				self.deviceState = "unpause"

				print("#### UNPAUSE")

			# end of command check

			# 작업 완료후 커맨드 초기화, deviceState 변경
			if (self.command != 0):
				self.command = 0
				firebase.put('/CONTROL', '/COMMAND', self.command)

			print(datetime.datetime.now())
			firebase.put('/CONTROL', '/DEVICESTATE', self.deviceState)

			if (self.deviceState == "running" and self.pauseFlag == False):
				self.checkMeasureTime = datetime.datetime.now()
				self.measurement()

			time.sleep(3)
			self.monitorCommand()

	# end of monitorCommand function

	def measurement(self):
		result = dwf.measureImpedance(self.setupData['channels'], self.setupData['freqs'])
		print(result)
		# firebase.put('/' + experiment_name, '/' + dataCounter, result)

	def saveLog(self, msg):
		firebase.put("/LOG", "/", msg)

# end of DeviceControl Class

if __name__ == "__main__":
	dc = DeviceControl()
	dc.monitorCommand()
