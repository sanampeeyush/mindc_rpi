from logge import generate_log as logger
import app
app.fetch()
logger('main file started')
try:
	import os
	import RPi.GPIO as pi
	import requests
	from time import sleep
	try:
		from vlc import MediaPlayer as mp
	except Exception as err:
		os.system('python3 -m pip install python-vlc')
		import vlc
		print('Error:',err)
		logger('REATTEMPTED ERROR::'+str(err))

	from audioDownloader import get_audio
	from datetime import datetime

	audio_path = '/home/pi/media/'
	pi.setmode(pi.BCM)
	buttons = [14,15,18,23,24,25,8,7,12,16]
	craddle_button = 20
	greenLed = 4
	flag = 0
	flag1 = 0
	temp = 0
	but = 0
	counter = 0
	for pin in buttons+[craddle_button]:
		pi.setup(pin, pi.IN, pull_up_down = pi.PUD_UP)

	pi.setup(greenLed, pi.OUT, initial=pi.LOW)

	if not get_audio():
		print('Error in Fetcing Audio')
		logger('ERROR::Error in Fetcing Audio')

	def debug_pins():
		for i in buttons+[craddle_button]:
			print(pi.input(i), end = ' ')
		print(' ')
	def buttonCheck():
		for ind,pin in enumerate(buttons):
			if not pi.input(pin) and not pi.input(craddle_button):
				while not pi.input(pin) and not pi.input(craddle_button):
					pass
				return ind+1
		return -1

	def buttonPlayAudio(num):
		idx = '';file = ''
		idx = str(num).zfill(2)
		date = datetime.now().strftime("%d-%m-%Y")
		file = f'{audio_path}/{idx}.mp3'
		print(file)
		playAudio(file)
	while True:
		try:
			idx = ''
			file = ''
			pi.output(greenLed, pi.HIGH)
			while not pi.input(craddle_button) and flag == 0:
				player = mp('/home/pi/abc.mp3')
				player.stop()
				sleep(0.2)
				player.play()
				sleep(0.2)
				print('play dialtone')
				but = buttonCheck()
				if but>0:
					flag = 1
					player.stop()
					sleep(0.2)
					try:
						player.release()
						sleep(0.2)
					except Exception as err:
						print("Err dialtone 1:",err)
					player = None
					print('stop playing dialtone')
					break
			while not pi.input(craddle_button) and flag == 1:
				if but>0:
					player = None
					idx = '';file=''
					idx = str(but).zfill(2)
					date = datetime.now().strftime('%d-%m-%Y')
					file = f'{audio_path}/{idx}.mp3'
					player = mp(file)
					player.stop()
					sleep(0.2)
					player.play()
					sleep(0.2)
					print(f'play {but} song')
				but = buttonCheck()
				while not pi.input(craddle_button) and but>0:
					player.stop()
					sleep(0.2)
					try:
						player.release()
						sleep(0.2)
					except Exception as err:
						print('Err in butt 2:',err)
					player = None
					print('stop playaig song')
					break
			while pi.input(craddle_button):
				flag = 0
				try:
					sleep(0.2)
					player.release()
					sleep(0.2)
				except Exception as err:
					print('CradleDownErr 3:',err)
				print('cradle down')
				break
		except Exception as err:
		    print('Error:',err)
		    logger('ERROR::'+str(err))

except Exception as err:
	print('Error:',err)
	logger('ERROR::'+str(err))
