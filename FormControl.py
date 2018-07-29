# coding: utf-8

import sys
from PyQt5 import QtWidgets
from PyQt5 import uic

from PyQt5.QtCore import pyqtSlot

from firebase.firebase import FirebaseApplication

class Form(QtWidgets.QDialog):
	global firebase
	global firebase_address

	firebase_address = "https://qttest0513.firebaseio.com/"

	"""

	"""
	def __init__(self, parent=None):
		QtWidgets.QDialog.__init__(self, parent)
		self.ui = uic.loadUi("MainForm.ui")
		self.ui.show()
		self.setupUI()

		# self.tdialog()
		self.initFirebase()

		self.channels = []
		self.freqs = []

	"""
	Firebase에 연결하여 firebase 변수에 저장.
	 * 재접속을 안해주고 약 50회 정도 그냥 시도하면 요청횟수 초과 오류가 발생함.
	"""
	def connectFirebase(self):
		global firebase
		firebase = FirebaseApplication(firebase_address)
		# https://qttest0513.firebaseio.com/

	"""
	Firebase의 '/CONTROL' 초기화
	**** 여기서 해주면 안됨. 최초 1회만 실행해야함
	"""
	def initFirebase(self):
		global firebase

		print(" ### Firebase initializing")
		self.connectFirebase()

		# CONTROL = {
		# 	'COMMAND': 0,
		# 	'DEVICESTATE': 'ready',
		# 	'RECORDSTATE': 'off',
		# 	'SETUP': 0,
		# 	'PAUSE': False,
		# }
		# firebase.put('/CONTROL', '/', CONTROL)

		print(" ### Init complete")

	"""
	Widget들 슬롯 연결
	"""
	def setupUI(self):
		self.ui.button_setup.clicked.connect(self.on_setup_click)
		self.ui.button_pause.clicked.connect(self.on_pause_click)
		self.ui.button_start.clicked.connect(self.on_start_click)
		self.ui.button_checkchip.clicked.connect(self.on_checkchip_click)
		self.ui.button_checkAll.clicked.connect(self.on_checkAll_click)

		self.ui.chkbox_ch1.stateChanged.connect(self.chkbox_ch_state)
		self.ui.chkbox_ch2.stateChanged.connect(self.chkbox_ch_state)
		self.ui.chkbox_ch3.stateChanged.connect(self.chkbox_ch_state)
		self.ui.chkbox_ch4.stateChanged.connect(self.chkbox_ch_state)
		self.ui.chkbox_ch5.stateChanged.connect(self.chkbox_ch_state)
		self.ui.chkbox_ch6.stateChanged.connect(self.chkbox_ch_state)
		self.ui.chkbox_ch7.stateChanged.connect(self.chkbox_ch_state)
		self.ui.chkbox_ch8.stateChanged.connect(self.chkbox_ch_state)

		self.ui.chkbox_freq4.stateChanged.connect(self.chkbox_freq_state)
		self.ui.chkbox_freq8.stateChanged.connect(self.chkbox_freq_state)
		self.ui.chkbox_freq16.stateChanged.connect(self.chkbox_freq_state)
		self.ui.chkbox_freq32.stateChanged.connect(self.chkbox_freq_state)

	"""
	firebase 연결 dialog
	주소를 입력받아 연결.
	"""
	def tdialog(self):
		# 클래스 만들어서 다시하기
		dialog = QtWidgets.QDialog()
		dialog.ui = uic.loadUi("popup.ui")
		dialog.ui.show()
		print("??????")

	"""
	채널 체크박스 상태 검사후 리스트에 추가하는 함수
	"""
	@pyqtSlot()
	def chkbox_ch_state(self):
		self.channels = []

		if (self.ui.chkbox_ch1.isChecked() == True):
			self.channels.append(0)
		if (self.ui.chkbox_ch2.isChecked() == True):
			self.channels.append(1)
		if (self.ui.chkbox_ch3.isChecked() == True):
			self.channels.append(2)
		if (self.ui.chkbox_ch4.isChecked() == True):
			self.channels.append(3)
		if (self.ui.chkbox_ch5.isChecked() == True):
			self.channels.append(4)
		if (self.ui.chkbox_ch6.isChecked() == True):
			self.channels.append(5)
		if (self.ui.chkbox_ch7.isChecked() == True):
			self.channels.append(6)
		if (self.ui.chkbox_ch8.isChecked() == True):
			self.channels.append(7)

		print(self.channels)

	"""
	주파수 체크박스 상태 검사후 리스트에 추가하는 함수
	"""
	@pyqtSlot()
	def chkbox_freq_state(self):
		self.freqs = []
		if (self.ui.chkbox_freq4.isChecked() == True):
			self.freqs.append(4000)
		if (self.ui.chkbox_freq8.isChecked() == True):
			self.freqs.append(8000)
		if (self.ui.chkbox_freq16.isChecked() == True):
			self.freqs.append(16000)
		if (self.ui.chkbox_freq32.isChecked() == True):
			self.freqs.append(32000)

		print(self.freqs)

	"""
	check all 버튼 클릭시 채널 체크박스를 모두 체크상태로 변경
	"""
	@pyqtSlot()
	def on_checkAll_click(self):
		self.ui.chkbox_ch1.setChecked(True)
		self.ui.chkbox_ch2.setChecked(True)
		self.ui.chkbox_ch3.setChecked(True)
		self.ui.chkbox_ch4.setChecked(True)
		self.ui.chkbox_ch5.setChecked(True)
		self.ui.chkbox_ch6.setChecked(True)
		self.ui.chkbox_ch7.setChecked(True)
		self.ui.chkbox_ch8.setChecked(True)

	"""
	SETUP 버튼 클릭시
	{채널, 주파수, 측정 간격, 기간, 실험명}을 입력했는지 확인 후
	Firebase에 전달.
	"""
	@pyqtSlot()
	def on_setup_click(self):
		global firebase
		print("setup button clicked")
		# 공백 검사하기.
		# 양식(자연수 등등) 확인하기
		period = self.ui.edit_period.text()
		deadline = self.ui.edit_deadline.text()
		name = self.ui.edit_name.text()

		if (period == ''):
			# 메세지박스로 바꾸기
			print("period is empty")
			return
		elif (deadline == ''):
			print("deadline is empty")
			return
		elif (name == ''):
			print("experiment name is empty")
			return

		if not self.channels:
			print('channels is empty')
			return

		if not self.freqs:
			print('freqs is empty')
			return

		settings = {
			'channels': str(self.channels),
			'freqs': str(self.freqs),
			'period': period,
			'deadline': deadline,
			'experiment_name': name
		}
		print(settings)

		getData = firebase.get('/CONTROL', None)
		tempKeys = [str(x) for x in getData.keys()]
		print(tempKeys)

		if (settings['experiment_name'] in tempKeys):
			print("실험명이 이미 존재합니다.")
		elif (getData['DEVICESTATE'] == 'ready'):
			command = 'setup'
			firebase.put('/CONTROL', 'SETUP', settings)
			firebase.put('/CONTROL', 'COMMAND', command)

	@pyqtSlot()
	def on_pause_click(self):
		# 토글버튼으로 바꿔줘야됨
		# pause, unpause
		if (self.ui.button_pause.getText() == pause)
		self.ui.button_pause.setText("unpause")

		firebase.put('/CONTROL', '/PAUSE', )
		print('test2')

	@pyqtSlot()
	def on_start_click(self):
		deviceState = firebase.get('/CONTROL/DEVICECSTATE', None)
		print("device state : ", deviceState)

		if (deviceState == 'setup'):
			command = 'start'
			firebase.put('/CONTROL', '/COMMAND', command)
			print("cytowatcher start")
		else:
			print("devicec not setup")

	@pyqtSlot()
	def on_checkchip_click(self):
		print('test4')

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	w = Form()
	sys.exit(app.exec_())
