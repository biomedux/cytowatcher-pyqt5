# coding: utf-8

from firebase.firebase import FirebaseApplication

import threading
import dwf

import copy

# firebase = FirebaseApplication("https://qttest0513.firebaseio.com/")

class DeviceControl():
	global firebase

	def __init__(self):
		self.firebase_address = "https://qttest0513.firebaseio.com/"
		self.tryCount = 0
		self.command = 0
		self.deviceState = 0
		self.recordState = 0
		self.pauseFlag = False
		# self.getSetup = {}
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

		firebase = FirebaseApplication(self.firebase_address)
		self.tryCount = 0
		# https://qttest0513.firebaseio.com/

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
			'RECORDSTATE': 'off',
			'SETUP': 0,
			'PAUSE': False,
		}
		firebase.put('/CONTROL', '/', CONTROL)

		print(" ### Init complete")


	def monitorCommand(self):
		global firebase

		self.tryCount += 1
		if (self.tryCount > 50):
			self.connectFirebase()

		try:
			getData = firebase.get('/CONTROL', None)
		except Exception as e:
			print(e, type(e))
			# self.monitorCommand()

		self.command = getData['COMMAND']
		self.deviceState = getData['DEVICESTATE']
		self.recordState = getData['RECORDSTATE']
		self.pauseFlag = getData['PAUSE']
		getSetup = getData['SETUP']

		# command별 동작
		if (self.command == 'checkchip'):
			print("!! CHECKCHIP command received")
			result = dwf.checkchip()
			firebase.put('/CHECKCHIP', '/', result)

		elif (self.command == 'start'):
			print("!! START command received")
			import datetime
			now = datetime.now()
			print(now)

			self.deviceState = 'running'

		elif (self.command == 'stop'):
			print("!! STOP command received")
			# 사용한거 다 초기화
			# deviceState ready로 변경
			# recordState off로 변경
			# firebase 초기화

			self.deviceState = "stop"
			self.initFirebase()

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

		elif (self.command == 'setup'):
			print("device setup")

			self.setupData = copy.deepcopy(getSetup)
			self.deviceState = 'setup'
			firebase.put('/' + self.setupData['experiment_name'], '/setup', self.setupData)

			print("setup data : ", self.setupData)

		# 작업 완료후 커맨드 초기화
		self.command = 0
		firebase.put('/CONTROL', '/DEVICESTATE', self.deviceState)
		firebase.put('/CONTROL', '/COMMAND', self.command)

		threading.Timer(5, self.monitorCommand).start()

	def measurement(self):
		while (self.pauseFlag == True):
			pass

		threading.Timer(self.setupData['interval'], self.).start()

	def saveLog(self, msg):
		firebase.put("/LOG", "/", msg)

if __name__ == "__main__":
	dc = DeviceControl()
	dc.monitorCommand()
	pass
