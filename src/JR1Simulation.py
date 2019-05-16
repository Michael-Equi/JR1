#!/usr/bin/env python
import numpy as np
import sys
from physicsSimulator import PhysicsObject

if(len(sys.argv) != 2):
    print("Usage error! Run program with thurst profile filepath argument")
    sys.exit(1)
else:
    filename = sys.argv[1]
    profile = np.loadtxt(filename, delimiter=",")

print("Welcome to the JR1 physics simulator")
print("Thrust profile filepath = " + filename)

#2.16in = 0.054864m
#See https://www.grc.nasa.gov/WWW/K-12/rocket/shaped.html for cd approximation as bullet
#assume no drag force in the x and y dimensions
rocket = PhysicsObject("JR1", 0.5, cd=[0,0,0.295], area=[0,0,0.054864], density=1.225, debug=False)

#wait until motor starts putting out 5 newtons
interaterStart = 0
while(profile[interaterStart,1] < 5):
    interaterStart += 1

print("Starting at index " + str(interaterStart))
rocket.iterationCounter = interaterStart


maxVelocity = 0
maxAltitude = 0

if(raw_input("Run simulation to apogee? Y/N").lower() == "y"):
    print("Running simulation to apogee...")
    while not rocket.velocity[2] < 0:
        rocket.applyForceFromArray(profile, mask=np.array([0,0,1]))
        rocket.takeStepFromArray(profile)
        if rocket.velocity[2] > maxVelocity:
            maxVelocity = rocket.velocity[2]
        if rocket.position[2] > maxAltitude:
            maxAltitude = rocket.position[2]

else:
    numSteps = input("Number of steps to run: ")
    print("Running steps: " + str(numSteps))
    for i in range(numSteps):
        rocket.applyForceFromArray(profile, mask=np.array([0,0,1]))
        rocket.takeStepFromArray(profile)
        if rocket.velocity[2] > maxVelocity:
            maxVelocity = rocket.velocity[2]
        if rocket.position[2] > maxAltitude:
            maxAltitude = rocket.position[2]

print("\n############################################")
print("Max altitude/apogee = " + str(maxAltitude))
print("Max velocity = " + str(maxVelocity))
