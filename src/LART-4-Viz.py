#!/usr/bin/env python

import numpy as np
import sys
import matplotlib.pyplot as plt

if(len(sys.argv) > 1):
        filename = sys.argv[1]
        profile = np.loadtxt(filename, delimiter=",")
        print("Shape of the data: " + str(profile.shape))
        plt.plot(profile[:,1])
        plt.show()

else:
    print("Please type file name when calling the program")
