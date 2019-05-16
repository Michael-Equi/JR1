#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

# class to handle saving an loading thrust information and time stamps
# will provide the functions to easily cycle through timesteps to run euler method based algorithms
class PhysicsObject():
    def __init__(self, name, mass, cd=[0,0,0], area=[1,1,1], density=1, g=[0,0,-9.80665], time=0, dt=0.001, debug=False):
        #units are kg,m,s
        self.name = name               #name of the object for printing
        self.mass = mass               #mass of the object
        self.cd = np.asarray(cd)       #the coefficient of drag (do not pass in area and density if "coefficient" includes those values)
        self. area = np.asarray(area)  #cross sectional area used for drag force calculations
        self.density = density         #density of the fluid that the object is moving through
        self.g = np.asarray(g)         #accleration due to gravity (should be negative for downward force of gravity in the z direction
        self.time = time               #current sim time in seconds
        self.dt = dt                   #amount of time between each step taken
        self.debug = debug             #wether or not to print out each step

        #to not apply gravity, set g to zero
        #convention is right, up, and forward are positive

        #state values x,y,z
        self.position = np.array(([0.0,0.0,0.0]))
        self.velocity =  np.array(([0.0,0.0,0.0]))
        self.acceleration = np.array(([0.0,0.0,0.0]))

        self.iterationCounter = 0 #for the take step from array

    def specialPrint(self, value, unit):
        #value = number
        #unit = m, m/s, m/s^2, N, Ns
        if self.debug:
            print(self.name + ": " + str(value) + unit + " at time " + str(self.time) + "s")

    def applyDrag(self):
        #special function for computing and applying drag
        # Fd = 1/2*Cp*A*Cd - https://en.wikipedia.org/wiki/Drag_(physics)
        # Ad = Fd/m
        #-1 and sign operation to get the correct direction of the acceleration
        accelerations = (-1*np.sign(self.velocity)*0.5*self.cd*self.density*self.area*np.square((self.velocity)))/self.mass
        self.addAcceleration(accelerations)

    def addForce(self, force):
        #force should be a numpy array with x,y,z and correct sign for direction
        self.accleration += (force/self.mass)

    def addAcceleration(self, acceleration):
        #force should be a numpy array with x,y,z and correct sign for direction
        self.acceleration += acceleration

    def takeStep(self):
        #updates velocity and position vectors based on accelerations and dt
        self.applyDrag()
        self.velocity += (self.acceleration + self.g)*self.dt
        self.position += self.velocity*self.dt

        self.specialPrint(self.acceleration + self.g, "m/s^2")
        self.specialPrint(self.velocity, "m/s")
        self.specialPrint(self.position, "m")

        #set acceleration vector back to zero
        self.acceleration = np.array(([0.0,0.0,0.0]))
        self.time += self.dt

    def takeStepFromArray(self, array):
        #function that loads in array and computes time steps from column 0
        if array.shape[0] > self.iterationCounter+1:
            self.dt = array[self.iterationCounter+1,0] - array[self.iterationCounter,0]
        self.takeStep()
        self.iterationCounter += 1

    def applyForceFromArray(self, array, mask=np.array([1,1,1])):
        #function that loads in array and computes time steps from column 1
        #mask allows the array to be a single value
        if array.shape[0] > self.iterationCounter:
            self.addAcceleration(array[self.iterationCounter, 1]*mask/self.mass)
