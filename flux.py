
import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.constants as sc
from pynput.keyboard import Listener, Key

def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press = next_image)
listener.start()

for i in range(1):
    f = open("/home/physics/phubjv/Lare2d-dev/Data/flux.dat", "r")
    lines = f.readlines()
    snb_flux = []
    sh_flux = []
    if (i == 0): diff = np.array([])
    for line in lines:
        split = line.split()
        snb_flux.append(float(split[0]))
        sh_flux.append(float(split[1]))
        
    snb_flux.pop()
    sh_flux.pop()
    
    y = np.linspace(0,170,num  = len(snb_flux))
    
    plt.plot(y,snb_flux, label = "snb" + str(i))
    if (i == 0): plt.plot(y, sh_flux, label = "flux-limiting")
    plt.legend()
    #if (i == 0): 
    #    diff = np.array(snb_flux)
    #else:
    #    diff = (np.array(snb_flux) - diff) /  max(diff) * 100

plt.show()

#plt.plot(y, diff)
#plt.show()
