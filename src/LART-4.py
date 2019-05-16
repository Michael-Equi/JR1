#!/usr/bin/env python

import sys, serial, math, time, signal, datetime
import numpy as np
import matplotlib.pyplot as plt

#function to save saveData
def saveData(data):
	file_name =  "data/" + str(datetime.datetime.now()) + ".csv"
	print("Data saved to " + file_name)
	np.savetxt(file_name, data, delimiter=",")

end = False
def signal_handler(sig, frame):
	global end, max, impulse
	end = True
	print("##############################################")
	print("Max thrust = " + str(max) + "N")
	print("Total Impulse = " + str(impulse) + "Ns")
	plt.plot(data[...,1])
	plt.show()
	plt.close('all')
	val = raw_input("Save profile Y/N?")
	if(val == "y"):
		saveData(data)
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def map(input, inMin, inMax, outMin, outMax):
    output = (input - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
    return output

def toNewtons(value, zero=0, k=385.279037, n=4, max=502, min=0): #k in N/m, n is number of springs with constant k, max/min are of the pot
	distance = map(-(value-zero), min, max, 0, 0.1) #in meters
	return n*k*distance

ser = serial.Serial(port='/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_855313037303519142D0-if00', baudrate=115200)
ser.readline()
time.sleep(1)
zero = int(ser.readline().replace('\n', '').strip())
print("Zero point = " + str(zero))

data = np.zeros((1,2))
max, impulse = 0, 0
print("Recording Started...")
startTime = time.time()

while not end:
	try:
		raw = int(ser.readline().replace('\n', '').strip())
	except:
		continue
	value = toNewtons(raw, zero)
	if(value - data[-1,1] < 100): #filter out erroneous values
		data = np.append(data, np.array([[time.time() - startTime, value]]), axis=0)
	if(value > max):
		max = value
	impulse += data[-1,1]*(data[-1,0]-data[-2,0])


# if(len(sys.argv) > 1):
# 	print("Reading from file: " + sys.argv[1])
# 	data = np.loadtxt(sys.argv[1], delimiter=',')
# else:
# 	sys.exit()
