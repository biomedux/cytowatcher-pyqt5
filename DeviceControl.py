# coding: utf-8

from firebase.firebase import FirebaseApplication

import threading
import dwf

# firebase = FirebaseApplication("")

class DeviceControl():
	global firebase

	def __init__(self):
		self.firebase_address = "https://qttest0513.firebaseio.com/"
		self.tryCount = 0
		self.command = 0
		self.deviceState = 0
		self.recordState = 0
		self.pauseFlag = False
		self.getSetup = {}
		self.setupData = {
			'channels': 0,
			'freqs': 0,
			'period': 0,
			'deadline': 0,
			'experiment_name': 0,
		}

		dwf.initialize()

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
			self.monitorCommand()

		command = getData['COMMAND']
		deviceState = getData['DEVICESTATE']
		recordState = getData['RECORDSTATE']
		getSetup = getData['SETUP']
		pauseFlag = getData['PAUSE']

		if (command == 'checkchip'):
			result = dwf.checkchip()
			firebase.put('/CHECKCHIP', '/', result)

		elif (command == 'start'):
			print("## start command received")

		elif (command == 'stop'):
			# 사용한거 다 초기화
			# deviceState ready로 변경
			# recordState off로 변경
			# firebase 초기화

			self.initFirebase()

		elif (command == 'pause'):
			pass

		elif (command == 'unpause'):
			pass

		elif (command == 'setup'):
			pass

		threading.Timer(5, self.monitorCommand).start()

	def measurement(self):
		pass

	def saveLog(self, msg):
		pass

if __name__ == "__main__":
	dc = DeviceControl()
	dc.monitorCommand()
	pass
