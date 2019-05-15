#!/usr/bin/env python

import sys, serial, math, time, signal
import numpy as np
import matplotlib.pyplot as plt
import numpy

end = False
def signal_handler(sig, frame):
	global end, max, impulse
	end = True
	print("##############################################")
	print("Max thrust = " + str(max) + "N")
	print("Total Impulse = " + str(impulse) + "Ns")
	plt.plot(x)
	plt.show()
	plt.close('all')
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def map(input, inMin, inMax, outMin, outMax):
    output = (input - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
    return output

def toNewtons(value, zero=0, k=385.279037, n=4, max=502, min=0): #k in N/m, n is number of springs with constant k, max/min are of the pot
	distance = map(value-zero, min, max, 0, 0.1) #in meters
	return 4*k*distance

ser = serial.Serial(port='/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_855313037303519142D0-if00', baudrate=115200)
ser.readline()
time.sleep(1)
zero = int(ser.readline().replace('\n', '').strip())
print("Zero point = " + str(zero))

data = np.zeros((0,2))
max, impulse = 0, 0
x = np.array((1))
lastPlotPoint = time.time()
print("Recording Started...")
while not end:
	try:
		ser.flushInput()
		value = toNewtons(int(ser.readline().replace('\n', '').strip()), zero)
		data = np.append(data, np.array([[time.time(), value]]), axis=0)

		if(value > max):
			max = value

		if(time.time() - lastPlotPoint > 0.1):
			x = np.append(x,[value])
			lastPlotPoint = time.time()

		impulse += data[-1,1]*(data[-1,0]-data[-2,0])

		time.sleep(0.001)

	except:
		pass


# if(len(sys.argv) > 1):
# 	print("Reading from file: " + sys.argv[1])
# 	data = np.loadtxt(sys.argv[1], delimiter=',')
# else:
# 	sys.exit()
