import multiprocessing
import speech_recognition as sr
import pyautogui
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

engine.setProperty('rate',175)

def speak_up(s):
	engine.say(s)
	engine.runAndWait()

def convert_to_words(num):
	outputString = ""
	l = len(num)
	if (l == 0):
		return outputString

	if (l > 4):
		return outputString
	single_digits = ["zero", "one", "two", "three","four", "five", "six", "seven","eight", "nine"]

	two_digits = ["", "ten", "eleven", "twelve","thirteen", "fourteen", "fifteen","sixteen", "seventeen", "eighteen","nineteen"]

	tens_multiple = ["", "", "twenty", "thirty", "forty","fifty", "sixty", "seventy", "eighty","ninety"]

	tens_power = ["hundred", "thousand"]

	if (l == 1):
		outputString += single_digits[ord(num[0]) - 48]
		return outputString

	x = 0
	while (x < len(num)):

		if (l >= 3):
			if (ord(num[x]) - 48 != 0):
				outputString += single_digits[ord(num[x]) - 48]+" "
				outputString += tens_power[l - 3]+" "
			l -= 1
		else:
			if (ord(num[x]) - 48 == 1):
				sum = (ord(num[x]) - 48 +
					ord(num[x+1]) - 48)
				outputString += two_digits[sum]
				return outputString
			elif (ord(num[x]) - 48 == 2 and
				ord(num[x + 1]) - 48 == 0):
				outputString += "twenty"
				return outputString
			else:
				i = ord(num[x]) - 48
				if(i > 0):
					outputString += tens_multiple[i]+" "
				else:
					outputString += ""
				x += 1
				if(ord(num[x]) - 48 != 0):
					outputString += single_digits[ord(num[x]) - 48]
		x += 1
	return outputString

# disable the pyautogui hot-positions
pyautogui.FAILSAFE = False

# storing a copy of screen size
scrX, scrY = pyautogui.size()
# preprocess for speech recognition
R = sr.Recognizer()

# hotwords
exitText  = "exit" 
right     = "right" 
left      = "left"
up        = "up"
down      = "down"
stop      = "stop"
speedUp   = "fast"
speedDown = "slow"
s_click   = "click"
d_click   = "double click"
r_click   = "right click"
hold      = "take"
release   = "leave"
cont_txt  = "continue"
u_scroll  = "scroll up"
d_scroll  = "scroll down"
silence   = "silence"
speak     = "october"

# endpoint delimeter in pixel position
endPoint = 0
# upper and lower bound to speed limit
topSpeed, bottomSpeed = 10, 1
# start-speed
startSpeed = 3

def mouse_movement(pSpeed, mFlag, eFlag, jFlag, sFlag, posX, posY):

	while(True):
		if(eFlag.value):
			return

		if(pSpeed.value>topSpeed):
			pSpeed.value = topSpeed
		if(pSpeed.value<bottomSpeed):
			pSpeed.value = bottomSpeed
		
		if(jFlag.value!=0):
			if(mFlag.value == 0):
				posX -= int(jFlag.value*scrX/100)
			elif(mFlag.value == 1): 
				posX += int(jFlag.value*scrX/100)
			elif(mFlag.value == 2): 
				posY -= int(jFlag.value*scrY/100)
			elif(mFlag.value == 4): 
				posY += int(jFlag.value*scrY/100)
			jFlag.value = 0
			mFlag.value = 5

		if(mFlag.value == 0):
			posX -= pSpeed.value
		elif(mFlag.value == 1): 
			posX += pSpeed.value
		elif(mFlag.value == 2): 
			posY -= pSpeed.value
		elif(mFlag.value == 4): 
			posY += pSpeed.value
		elif(mFlag.value == 6):
			pyautogui.click(posX, posY) 
			mFlag.value = 5
		elif(mFlag.value == 7):
			pyautogui.click(posX, posY) 
			pyautogui.click(posX, posY) 
			mFlag.value = 5
		elif(mFlag.value == 8):
			pyautogui.mouseDown() 
			mFlag.value = 5
		elif(mFlag.value == 9):
			pyautogui.mouseUp() 
			mFlag.value = 5
		elif(mFlag.value == 10):
			pyautogui.rightClick() 
			mFlag.value = 5
		elif(mFlag.value == 11):
			if(sFlag.value!=0): 
				pyautogui.scroll(int(sFlag.value*scrY/100))
			else: 
				pyautogui.scroll(100)
			mFlag.value = 5
		elif(mFlag.value == 12):
			if(sFlag.value!=0): 
				pyautogui.scroll(int(-1*sFlag.value*scrY/100))
			else: 
				pyautogui.scroll(-100)
			mFlag.value = 5

		if(posX<endPoint):
			posX = endPoint
		if(posY<endPoint):
			posY = endPoint
		if(posX>scrX):
			posX = scrX
		if(posY>scrY):
			posY = scrY
		
		pyautogui.moveTo(posX, posY)

def get_mic():
   try:
      source = sr.Microphone()
      return source
   except OSError:
      return None

def get_command(mFlag, pSpeed, eFlag, jFlag, sFlag, rFlag):

	# history for storing the previous operation = for continue
	hist = 5

	Source = get_mic()
	if not Source:
		print("No Mic Device Found!")
		exit()

	while(True):
		text = "Nil"

		with Source as source:

			if(eFlag.value):
				return

			audio = R.listen(source, phrase_time_limit=3)
			try:
				text = R.recognize_google(audio).lower()
				print("Did you said '"+text+"' ?")
			except:
				print("I'm Listening")
				text = stop

			if(cont_txt in text):
				mFlag.value = hist
				continue

			if(exitText in text):
				eFlag.value = 1;
			if(left in text):
				mFlag.value = 0;
			if(right in text):
				mFlag.value = 1;
			if(up in text):
				mFlag.value = 2;
			if(down in text):
				mFlag.value = 4;
			
			if(speedUp in text):
				pSpeed.value += 1
			if(speedDown in text):
				pSpeed.value -= 1

			if(s_click in text):
				mFlag.value = 6
			if(d_click in text):
				mFlag.value = 7
			if(hold in text):
				mFlag.value = 8
			if(release in text):
				mFlag.value = 9
			if(r_click in text):
				mFlag.value = 10
			if(u_scroll in text):
				mFlag.value = 11
			if(d_scroll in text):
				mFlag.value = 12

			if(silence in text):
				rFlag.value = 1
			if(speak in text):
				rFlag.value = 0

			if(stop in text):
				mFlag.value = 5;

			jFlag.value = 0
			for i in range(0,101):
				if(str(i) in text or str(convert_to_words(str(i))) in text):
					jFlag.value = i;
			if('100' in text or 'hundred' in text):
				jFlag.value = 100

			if(mFlag.value in [11,12]):
				sFlag.value = jFlag.value
				jFlag.value = 0

			# history of the operations
			if mFlag.value in [0,1,2,4,11,12]:
				hist = mFlag.value
		
def relay_situation(mFlag, eFlag, rFlag, pSpeed):
	myFlag = 5
	myVoice = 0
	mySpeed = startSpeed
	while(True):
		# a simple fairwell
		if(eFlag.value): 
			speak_up("Thank you for giving me a try. Its October signing off, Have a good day ahead!")
			return

		if(myFlag != mFlag.value and not rFlag.value):
			myFlag = mFlag.value

			if(myFlag==0):speak_up("Going Left")
			if(myFlag==1):speak_up("Going Right")
			if(myFlag==2):speak_up("Going Up")
			if(myFlag==4):speak_up("Going Down")

			if(myFlag==6):speak_up("Single click")
			if(myFlag==7):speak_up("Double click")
			if(myFlag==8):speak_up("holding left click")
			if(myFlag==9):speak_up("releasing left click")
			if(myFlag==10):speak_up("right click")
			if(myFlag==11):speak_up("scrolling up")
			if(myFlag==12):speak_up("scrolling down")

		if(mySpeed!=pSpeed.value and not rFlag.value):
			if(mySpeed<pSpeed.value):
				speak_up("Speeding up")
			else:
				speak_up("going slower")
			mySpeed = pSpeed.value

		if(myVoice != rFlag.value):
			myVoice = rFlag.value
			if(myVoice == 1):
				speak_up("I am going for a little nap. See you soon.")
			else:
				speak_up("I am here!! October is back in your life!")

def introduction():
	# introduction
	speak_up("Hello, I'm October, I'm your virtual mouse. I can do everything, that a physical mouse or a track-pad can do. So, lets get going.")

if __name__ == '__main__':
	# storing current mouse position
	posX, posY = pyautogui.position()

	# movement flag
	# 0:Left, 1:Right, 2:Up, 4:Down, 5:Stay
	# 6:Single-Click 7:Double-Click 8:hold 9:release
	# 10:right-click 11:scroll-up 12:scroll-down
	# 13:turning-off-assistant 14:turning-on-assistant
	manager = multiprocessing.Manager()
	mFlag = manager.Value('i', 5)

	# pointer speed 
	pSpeed = manager.Value('i', startSpeed)

	# fatal Flag to end the simulation
	eFlag = manager.Value('i', 0)

	# jump Flag to jump the number of pixels
	jFlag = manager.Value('i', 0)

	# scroll Flag
	sFlag = manager.Value('i', 0)

	# Flag to toggle voice assistant
	rFlag = manager.Value('i', 0)

	operation0 = multiprocessing.Process(target=introduction)
	operation1 = multiprocessing.Process(target=get_command, args=[mFlag, pSpeed, eFlag, jFlag, sFlag, rFlag])
	operation2 = multiprocessing.Process(target=mouse_movement, args=[pSpeed, mFlag, eFlag, jFlag, sFlag, posX, posY])
	operation3 = multiprocessing.Process(target=relay_situation, args=[mFlag, eFlag, rFlag, pSpeed])

	operation0.start()
	operation1.start()
	operation2.start()
	operation3.start()
	operation0.join()
	operation1.join()
	operation2.join()
	operation3.join()

	