# coding: utf-8

from firebase.firebase import FirebaseApplication

import threading
import dwf
import datetime

import copy

class DeviceControl():
	global firebase

	def __init__(self):
		self.firebase_address = "https://qttest0513.firebaseio.com/"
		self.tryCount = 0
		self.command = 0
		self.deviceState = 0
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

		try:
			getData = firebase.get('/CONTROL', None)
		except Exception as e:
			print("firebase connection error.. retry")
			self.connectFirebase()
			self.monitorCommand()

		self.command = getData['COMMAND']
		self.pauseFlag = getData['PAUSE']
		getSetup = getData['SETUP']

		# command check
		if (self.command == 'checkchip'):
			print("!! CHECKCHIP command received")
			result = dwf.checkChip()
			firebase.put('/CHECKCHIP', '/', result)

		elif (self.command == 'setup'):
			print("!! SETUP command received")

			self.setupData = copy.deepcopy(getSetup)
			self.deviceState = 'setup'
			firebase.put('/' + self.setupData['experiment_name'], '/setup/', self.setupData)

			print("setup data : ", self.setupData)

		elif (self.command == 'start'):
			print("!! START command received")
			now = datetime.now()
			print(now)

			self.deviceState = 'running'

		elif (self.command == 'stop'):
			# measurement 중지시키고 파이어베이스 초기화해야됨
			print("!! STOP command received")

			# self.deviceState = "stop"
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

		# end of command check

		# 작업 완료후 커맨드 초기화, deviceState 변경
		self.command = 0
		try:
			print(datetime.datetime.now())
			firebase.put('/CONTROL', '/DEVICESTATE', self.deviceState)
			firebase.put('/CONTROL', '/COMMAND', self.command)
		except Exception as e:
			print("aaaaaaaa@@@@@@@@")
			print(e)

		time.sleep(5)
		self.monitorCommand()

	# end of monitorCommand function

	def measurement(self):
		while (self.pauseFlag == True):
			pass

		threading.Timer(self.setupData['interval'], self.measurement).start()

	def saveLog(self, msg):
		firebase.put("/LOG", "/", msg)

# end of DeviceControl Class

if __name__ == "__main__":
	dc = DeviceControl()
	dc.monitorCommand()
